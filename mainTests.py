from convertors.objects_definition import Node, Nu, NonP2pLinkProperties, Ip, Address, Ncs, P, Wpr, Pr, Res, Link, IpV6
from convertors.xml_reader import call_xml_parser
from gui import window
from utils.manager import get_objects_by_type

# Allowed tests in current state
allowed_tests_config = {
    "initialize_window_test": True,
    "none_type_test": True,
    "retrieve_objects_test": True,
    "parsing_test": True,
    "show_nodes_test": True,
    "simulate_communication_test": True,
    "arc_test": True
}

resources_path = 'resources/'

# List of possible objects
object_test_types = [Node, Nu, NonP2pLinkProperties, Ip, Address, Ncs, P, Wpr, Pr, Res, Link, IpV6]


# Code that is testing if count of unknown tags are zero
def none_type_test(none_type, filename):
    if allowed_tests_config["none_type_test"] is False:
        return
    assert none_type == 0, "Parsing test failed for file " + filename + " - none type should be zero!"


# Testing parsing of file from resources
def parsing_test(filename):
    if allowed_tests_config["parsing_test"] is False:
        return
    parsed_xml, none_type = call_xml_parser(filename)

    # Tests
    none_type_test(none_type, filename)

    retrieve_objects_test(parsed_xml.content, filename)
    return parsed_xml


# Testing displaying window
def initialize_window_test():
    if allowed_tests_config["initialize_window_test"] is False:
        return
    window.initialize_window()


# Testing functionality to get objects from parsing
def retrieve_objects_test(objects, filename):
    if allowed_tests_config["retrieve_objects_test"] is False:
        return
    for object_type in object_test_types:
        objects_result = get_objects_by_type(objects, object_type)
        for item in objects_result:
            assert isinstance(item, object_type), "Retrieve objects test failed for file " + filename + \
                                                  " - " + type(item) + " not equals " + type(object_type)


# Initialization function of tests
if __name__ == '__main__':
    # Parsing tests
    first_test_data = parsing_test(resources_path + "jj.xml")
    second_test_data = parsing_test(resources_path + "cc.xml")
    third_test_data = parsing_test(resources_path + "ns3.xml")

    # Window should be displayed
    initialize_window_test()

    # Window tests
    dataset_test = [first_test_data, second_test_data, third_test_data]
