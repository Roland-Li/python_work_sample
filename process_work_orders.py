import csv

# Preset Variables
order_file_name = "orders.txt"
dependency_file_name = "dependencies.txt"
output_file_name = "output.txt"
output_delimiter = " " * 3  # Specify the change the spacing of the output

# Hard-code a limit; works around possible cycles within the data; at least print _something_
depth_limit = 100

# Reads the orders from input texts
# RETURNS: dictionary(order_id, name), dictionary(order_id, child_id), set(dependant_nodes)
def read_orders():
    print("Reading orders")

    # This is what we're returning
    # order_names = dict() # Defined later
    # dependencies = dict() # Defined later
    global dependant_nodes  # Could have avoided doing this if I didn't define all these helper functions
    dependant_nodes = set()

    # Define a bunch of helper functions to reduce code usage (Just to 'flex' that I can, honestly)

    # Function for adding orders; when adding to dict, don't allow duplicates
    def add_to_dict_order(key, val, dict, file_name):
        if key in dict:
            print("WARNING: Encountered the same id in {}, overwriting {} with {}"
                  .format(file_name, dict[key], val))

        # Add it to the dict
        dict[key] = val

    # Function for adding dependencies; allow duplicates and keep track of dependant nodes
    def add_to_dict_dependency(key, val, dict, file_name):
        # Track the dependency
        dependant_nodes.add(val)

        # Add the val to the dict differently depending on if it already exists; save memory from making a list
        if key not in dict:
            dict[key] = val
        else:
            try:
                # Extend, just add the new value
                dict[key].append(val)
            except AttributeError:
                # Extend, add old value and new value to a list
                dict[key] = [dict[key], val]

    # Function for reading a file and adding stuff to a dict; runs func to actually add
    def read_to_dict(file_name, add_to_dict_func):
        new_dict = dict()

        # Open the order file and extract the data
        order_file_obj = open(file_name, 'r')
        reader = csv.reader(order_file_obj, delimiter=',')

        # Try and skip the top row
        next(reader)

        # Loop over every line and add the contents
        for row in reader:
            # Sanity check for row parts; skip if invalid segment
            if len(row) < 2:
                continue

            # Run the custom function
            add_to_dict_func(row[0], row[1], new_dict, file_name)

        print("Finished reading file: {}".format(file_name))

        return new_dict

    # Run the helper function and get the data
    order_names = read_to_dict(order_file_name, add_to_dict_order)
    dependencies = read_to_dict(dependency_file_name, add_to_dict_dependency)

    return order_names, dependencies, dependant_nodes

# Outputs the orders
# INPUTS: dictionary(order_id, name), dictionary(order_id, child_id)
# OUTPUTS: writes hierarchy to a text file, name defined val: output_file_name, set(dependant_nodes)
# RETURNS: nothing
def output_orders(order_names, dependencies, dependant_nodes):
    print("Outputting order hierarchy:\n")

    # Output file
    order_file_obj = open(output_file_name, 'w')

    # Simple function to recursively print children
    def rec_output(order_id, depth):
        # Print some text for the current order level
        order_text = output_delimiter * depth + "Id: {}, Name: {}".format(order_id, order_names[order_id])
        print(order_text)
        order_file_obj.write(order_text + '\n')

        # Check if there are dependencies for this order
        if order_id in dependencies:
            # Safety check if we have too many layers
            if depth > depth_limit:
                print("WARNING: Depth exceeded hard-coded limit. Is there a cycle?")
                order_file_obj.write(output_delimiter * depth + "..." + '\n')
                return

            # Print some text to indicate the start of a child section
            dependency_text = output_delimiter * depth + "Dependencies"
            print(dependency_text)
            order_file_obj.write(dependency_text + '\n')

            # Loop over all the children and have them print as well
            for child_id in dependencies[order_id]:
                rec_output(child_id, depth+1)

    # Loop over all the top-level orders and recursive print their children
    for order_id in order_names:
        if order_id not in dependant_nodes:
            rec_output(order_id, 0)

    order_file_obj.close()
    print("Output saved to: {}".format(output_file_name))

# The main function that strings things together
def main():
    order_names, dependencies, dependant_orders = read_orders()
    output_orders(order_names, dependencies, dependant_orders)
    print("Finished running")

if __name__ == "__main__": main()

