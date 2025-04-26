const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
app.commandLine.appendSwitch('enable-software-rasterizer');

function createWindow() {
  const win = new BrowserWindow({
    width: 1100,
    height: 720,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog({ properties: ['openDirectory'] });
  return result.filePaths[0] || '';
});

ipcMain.on('analyze-repo', (event, config) => {
  const scriptPath = path.join(__dirname, 'run_analysis.py');
  const args = [
    `--repo_path=${config.repoPath}`,
    `--use_stat=${config.useStat}`,
    `--ai_summary=${config.aiSummary}`,
    `--test_mode=${config.testMode}`,
    `--api_key=${config.apiKey}`,
  ];

  const py = spawn('python', [scriptPath, ...args]);

  py.stdout.on('data', (data) => {
    event.sender.send('analysis-output', data.toString());
  });

  py.stderr.on('data', (data) => {
    event.sender.send('analysis-output', `[stderr] ${data.toString()}`);
  });

  py.on('close', (code) => {
    event.sender.send('analysis-output', `✅ Analysis finished with code ${code}`);
  });
});
