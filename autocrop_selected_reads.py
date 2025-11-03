def autocrop_selected_reads():
    """For each selected read node:
        - delete the already existing AutoCrop node
        - select the read
        - launch nukescripts.autocrop()
    """
    #Select nodes that are Read nodes only
    reads_selection = [node for node in nuke.selectedNodes() if node.Class() == "Read"]
    if not reads_selection:
        nuke.message("No Read nodes selected.")
        return
    #For each Read node select the downstream node
    for read in reads_selection:
        downstream = read.dependent()
        selection = downstream[0]
        #check if the downstream node is an AutoCrop and delete it
        if 'label' in selection.knobs() and selection['label'].value().strip() == "AutoCrop":
            nuke.delete(selection)
        #set the selection back to the Read nodes
        for all_nodes in nuke.allNodes():
            all_nodes.setSelected(0)
        read.setSelected(1)
        #run the nukescripts.autocrop()
        try:
            nukescripts.autocrop()
        except Exception as ex:
            nuke.message("Autocrop failed for '{}':\n{}".format(read.name(), ex))

    nuke.message("Autocrop done for {} Read node(s).".format(len(reads_selection)))

if __name__ == "__main__":
    autocrop_selected_reads()