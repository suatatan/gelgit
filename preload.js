const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  startAnalysis: (config) => ipcRenderer.send('analyze-repo', config),
  onOutput: (callback) => ipcRenderer.on('analysis-output', (_event, value) => callback(value))
});
