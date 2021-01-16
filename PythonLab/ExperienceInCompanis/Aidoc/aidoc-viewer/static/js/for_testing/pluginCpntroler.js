var PluginSelection = document.getElementById("PluginSelection");
for (var plugin_name in aidocViewer.plugins){
    var option = document.createElement("option");
    option.text = plugin_name;
    PluginSelection.add(option);
}

var load_dicom_plugin;
function submittingForm(theForm) {
  load_dicom_plugin.load_DICOM(theForm.workItem.value,
                  theForm.seriesKey.value,
                  parseInt(theForm.sliceNumber.value));
}

function ChangePlugin(){
    var selected_plugin = PluginSelection.options[PluginSelection.selectedIndex].value;
    load_dicom_plugin = aidocViewer.plugins[selected_plugin];
    load_dicom_plugin.reset();
}

ChangePlugin();