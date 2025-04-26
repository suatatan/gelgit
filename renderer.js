window.addEventListener('DOMContentLoaded', () => {
  const output = document.getElementById('output');

  document.getElementById('browseBtn').addEventListener('click', async () => {
    const selected = await window.electronAPI.selectFolder();
    document.getElementById('repoPath').value = selected;
  });

  document.getElementById('analyzeBtn').addEventListener('click', async () => {
    output.textContent = "🔄 Analyzing...";
    const config = {
      repoPath: document.getElementById('repoPath').value,
      useStat: document.getElementById('useStat').checked,
      aiSummary: document.getElementById('aiSummary').checked,
      testMode: document.getElementById('testMode').checked,
      apiKey: document.getElementById('apiKey').value
    };
    window.electronAPI.startAnalysis(config);
  });

  window.electronAPI.onOutput((line) => {
    output.textContent += line;
    output.scrollTop = output.scrollHeight;
  });
});
