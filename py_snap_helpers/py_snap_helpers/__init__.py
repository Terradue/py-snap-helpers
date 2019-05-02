
import lxml.etree as etree
import subprocess
import tempfile
import time
import psutil
import os
import snappy 
from snappy import GPF

class GraphProcessor():
    
    def __init__(self, wdir='.'):
        self.root = etree.Element('graph')
    
        version = etree.SubElement(self.root, 'version')
        version.text = '1.0'
        self.pid = None
        self.p = None
        self.wdir = wdir
   
    def view_graph(self):
        
        print(etree.tostring(self.root , pretty_print=True))
        
    def add_node(self, node_id, operator, parameters, source):
    
        xpath_expr = '/graph/node[@id="%s"]' % node_id

        if len(self.root.xpath(xpath_expr)) != 0:

            node_elem = self.root.xpath(xpath_expr)[0]
            operator_elem = self.root.xpath(xpath_expr + '/operator')[0]
            sources_elem = self.root.xpath(xpath_expr + '/sources')[0]
            parameters_elem = self.root.xpath(xpath_expr + '/parameters')

            for key, value in parameters.iteritems():
                
                if key == 'targetBandDescriptors':
                                        
                    parameters_elem.append(etree.fromstring(value))
                    
                else:
                    p_elem = self.root.xpath(xpath_expr + '/parameters/%s' % key)[0]

                    if value is not None:             
                        if value[0] != '<':
                            p_elem.text = value
                        else:
                            p_elem.text.append(etree.fromstring(value))
    
        else:

            node_elem = etree.SubElement(self.root, 'node')
            operator_elem = etree.SubElement(node_elem, 'operator')
            sources_elem = etree.SubElement(node_elem, 'sources')

            if isinstance(source, list):

                for index, s in enumerate(source):
                    if index == 0:  
                        source_product_elem = etree.SubElement(sources_elem, 'sourceProduct')

                    else: 
                        source_product_elem = etree.SubElement(sources_elem, 'sourceProduct.%s' % str(index))

                    source_product_elem.attrib['refid'] = s

            elif source != '':
                source_product_elem = etree.SubElement(sources_elem, 'sourceProduct')
                source_product_elem.attrib['refid'] = source

            parameters_elem = etree.SubElement(node_elem, 'parameters')
            parameters_elem.attrib['class'] = 'com.bc.ceres.binding.dom.XppDomElement'

            for key, value in parameters.iteritems():

                if key == 'targetBandDescriptors':
                                        
                    parameters_elem.append(etree.fromstring(value))
                    
                else:
                
                    parameter_elem = etree.SubElement(parameters_elem, key)

                    if value is not None:             
                        if value[0] != '<':
                            parameter_elem.text = value
                        else:
                            parameter_elem.append(etree.fromstring(value))

        node_elem.attrib['id'] = node_id

        operator_elem.text = operator 

    def save_graph(self, filename):
        
        with open(filename, 'wb') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write(etree.tostring(self.root, pretty_print=True))
     
    def plot_graph(self):
        
        for node_id in self.root.xpath('/graph/node/@id'):
            

            xpath_expr = '/graph/node[@id="%s"]' % node_id
            
            if len(self.root.xpath(xpath_expr + '/sources/sourceProduct')) != 0:
                print(self.root.xpath(xpath_expr + '/sources/sourceProduct'))[0].attrib['refid']
                print(node_id)
            else:
                print(node_id)
        return True
    
    def run(self):
        
        os.environ['LD_LIBRARY_PATH'] = '.'
        
        print('Processing the graph')
        
        fd, path = tempfile.mkstemp()
        
        try:
        
            self.save_graph(filename=path)
            options = ['/opt/snap/bin/gpt',
               '-x',
               '-c',
               '2048M',
               path]

            p = subprocess.Popen(options,
                stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            print('Process PID: %s' % p.pid)
            res, err = p.communicate()
            print (res, err)
        finally:
            os.remove(path)
            
            print('Done.')
        
def get_snap_parameters(operator):
    
    op_spi = GPF.getDefaultInstance().getOperatorSpiRegistry().getOperatorSpi(operator)

    op_params = op_spi.getOperatorDescriptor().getParameterDescriptors()

    return op_params

def get_operator_default_parameters(operator):
    
    parameters = dict()

    for param in get_snap_parameters(operator):
    
        parameters[param.getName()] = param.getDefaultValue()
    
    return parameters

def get_operator_help(op):
    
        op_spi = GPF.getDefaultInstance().getOperatorSpiRegistry().getOperatorSpi(op)
        
        print('Operator name: {}'.format(op_spi.getOperatorDescriptor().getName()))
        
        print('Operator alias: {}\n'.format(op_spi.getOperatorDescriptor().getAlias()))
        print('Parameters:\n')
        param_Desc = op_spi.getOperatorDescriptor().getParameterDescriptors()
        
        for param in param_Desc:
            print('{}: {}\nDefault Value: {}\n'.format(param.getName(),
                                                       param.getDescription(),
                                                       param.getDefaultValue()))
            
            print('Possible values: {}\n').format(list(param.getValueSet()))
            
            
def backscatter(**kwargs):
   
    options = dict()
    
    operators = ['Read', 
                 'ThermalNoiseRemoval', 
                 'Apply-Orbit-File',
                 'Calibration',
                 'Speckle-Filter',
                 'Multilook',
                 'LinearToFromdB',
                 'Terrain-Correction',
                 'Subset',
                 'Write']
    
    for operator in operators:
            
        print('Getting default values for Operator {}'.format(operator))
        parameters = get_operator_default_parameters(operator)
        
        options[operator] = parameters

    for key, value in kwargs.items():
        
        print('Updating Operator {}'.format(key))
        options[key.replace('_', '-')].update(value)
    
    mygraph = GraphProcessor()
    
    for index, operator in enumerate(operators):
    
        print('Adding Operator {} to graph'.format(operator))
        if index == 0:            
            source_node_id = ''
        
        else:
            source_node_id = operators[index - 1]
        
        mygraph.add_node(operator,
                         operator, 
                         options[operator], source_node_id)
    
    mygraph.view_graph()
    
    mygraph.run()
    
    
def op_help(op):
    
        op_spi = snappy.GPF.getDefaultInstance().getOperatorSpiRegistry().getOperatorSpi(op)
        
        print('Operator name: {}'.format(op_spi.getOperatorDescriptor().getName()))
        
        print('Operator alias: {}\n'.format(op_spi.getOperatorDescriptor().getAlias()))
        print('Parameters:\n')
        param_Desc = op_spi.getOperatorDescriptor().getParameterDescriptors()
        
        for param in param_Desc:
            print('{}: {}\nDefault Value: {}\n'.format(param.getName(),
                                                       param.getDescription(),
                                                       param.getDefaultValue()))
            
            print('Possible values: {}\n').format(list(param.getValueSet()))
