#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/splintered-reality/py_trees/devel/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
A py_trees demo.

.. argparse::
   :module: py_trees.demos.selector
   :func: command_line_argument_parser
   :prog: py-trees-demo-selector

"""
##############################################################################
# Imports
##############################################################################

import time
import py_trees


F_STATUS = py_trees.common.Status.FAILURE
R_STATUS = py_trees.common.Status.RUNNING
S_STATUS = py_trees.common.Status.SUCCESS

##############################################################################
# Classes
##############################################################################


def description() -> str:
    """
    Print description and usage information about the program.

    Returns:
       the program description string
    """
    content = (
        "Higher priority switching and interruption in the children of a selector.\n"
    )
    content += "\n"
    content += "In this example the higher priority child is setup to fail initially,\n"
    content += "falling back to the continually running second child. On the third\n"
    content += (
        "tick, the first child succeeds and cancels the hitherto running child.\n"
    )
    return content

def create_node(name_str,status_list,final_status=S_STATUS) -> py_trees.behaviours.StatusQueue:
    ''' create a node with multiple status queue '''
    return py_trees.behaviours.StatusQueue(name=name_str,queue=status_list,eventually=final_status)
    
def create_root() -> py_trees.behaviour.Behaviour:
    """ Create the root behaviour and it's subtree.
    Returns:
        the root behaviour
    """
    root = py_trees.composites.Selector(name="SelectorRoot", memory=False)
    ffs = create_node("Fail 2 Success",[F_STATUS,F_STATUS,S_STATUS])
    always_running = py_trees.behaviours.Running(name="Always Running")
    root.add_children([ffs, always_running])
    return root


##############################################################################
# Main
##############################################################################


def main() -> None:
    """Entry point for the demo script."""
    print(description())
    py_trees.logging.level = py_trees.logging.Level.DEBUG
    root = create_root()

    ####################
    # Execute
    ####################
    root.setup_with_descendants()
    for i in range(1, 5):
        try:
            print(f"\n==================== Tick {i} ====================\n")
            print('Tree status before the current ticking...')
            print(py_trees.display.unicode_tree(root=root, show_status=True))
            print('Ticking from the root node...')
            root.tick_once()
            print("\n")
            print('Tree status after the current ticking...')
            print(py_trees.display.unicode_tree(root=root, show_status=True))
            time.sleep(1.0)
        except KeyboardInterrupt:
            break
    print("\n")

if __name__ == '__main__':
    main()