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
   :module: py_trees.demos.sequence
   :func: command_line_argument_parser
   :prog: py-trees-demo-sequence
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
    content = "Demonstrates sequences in action.\n\n"
    content += (
        "A sequence is populated with 2-tick jobs that are allowed to run through to\n"
    )
    content += "completion.\n"
    return content

def create_node(name_str,action_list,final_state=S_STATUS) -> py_trees.behaviours.StatusQueue:
    '''
    create a node that will eventually success
    '''
    return py_trees.behaviours.StatusQueue(name=name_str,
                                           queue=action_list,
                                           eventually=final_state)

def create_root() -> py_trees.behaviour.Behaviour:
    """
    Create the root behaviour and it's subtree.

    Returns:
        the root behaviour
    """
    root = py_trees.composites.Sequence(name="SequenceRoot", memory=True)
    for action in ["Job 1", "Job 2", "Job 3"]:
        act = create_node(action,[R_STATUS,S_STATUS])
        root.add_child(act)
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
    for i in range(1, 6):
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