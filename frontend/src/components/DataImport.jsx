import { useState } from "react";
import { importFile } from "../router";
import { TEXT } from "../constants/text";
import "..//css/DataImport.css";

export default function DataImport({ onImported }) {
  const [importUrl, setImportUrl] = useState("");
  const [importing, setImporting] = useState(false);
  const [importError, setImportError] = useState("");

  async function handleFileImport(e) {
    const file = e.target.files[0];
    if (!file) return;

    setImporting(true);
    setImportError("");
    try {
      const response = await importFile(file);
      console.log("response: ",response)
      await onImported(response);
    } catch (err) {
      setImportError(TEXT.dataImport.importError);
    } finally {
      setImporting(false);
      e.target.value = "";
    }
  }

  return (
    <div className="data-import">
      <label className="data-import__file-label">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileImport}
          disabled={importing}
          className="data-import__file-input"
        />
        <span className="data-import__file-button">{TEXT.dataImport.fileButton}</span>
      </label>


      {importing && <span className="data-import__status">{TEXT.dataImport.importing}</span>}
      {importError && <span className="data-import__error">{importError}</span>}
    </div>
  );
}
