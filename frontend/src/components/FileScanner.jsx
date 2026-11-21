import { useRef, useState } from "react";
import { motion } from "framer-motion";
import {
  Upload,
  FileText,
  ShieldCheck,
  ShieldAlert,
  LoaderCircle,
  Download,
  Trash2,
  ScanSearch,
  AlertTriangle,
} from "lucide-react";

import { uploadFiles } from "../services/api";
import "./FileScanner.css";

function FileScanner() {
  const fileInput = useRef(null);

  const [selectedFiles, setSelectedFiles] = useState([]);
  const [results, setResults] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState("");

  const allowedExtensions = [
    ".pdf", ".txt", ".csv", ".json",
    ".py", ".js", ".java", ".log",
  ];

  const addFiles = (incomingFiles) => {
    const validFiles = Array.from(incomingFiles).filter((file) => {
      const extension = "." + file.name.split(".").pop().toLowerCase();
      return allowedExtensions.includes(extension);
    });

    setSelectedFiles((previous) => {
      const combined = [...previous, ...validFiles];
      return combined.filter(
        (file, index, array) =>
          array.findIndex(
            (item) => item.name === file.name && item.size === file.size
          ) === index
      ).slice(0, 10);
    });

    setError("");
    setResults(null);
  };
  const handleFileChange = (event) => {
    addFiles(event.target.files);
    event.target.value = "";
  };

  const removeFile = (index) => {
    setSelectedFiles((previous) =>
      previous.filter((_, fileIndex) => fileIndex !== index)
    );
  };

  const clearFiles = () => {
    setSelectedFiles([]);
    setResults(null);
    setError("");
  };
    const handleDrop = (event) => {
    event.preventDefault();
    addFiles(event.dataTransfer.files);
  };
    const handleScan = async () => {
    if (selectedFiles.length === 0) {
      setError("Please select at least one file.");
      return;
    }

    setIsScanning(true);
    setError("");
    setResults(null);

    try {
      const data = await uploadFiles(selectedFiles);
      setResults(data);
    } catch (scanError) {
      setError(
        scanError.response?.data?.detail ||
        scanError.message ||
        "Scanning failed. Please check your backend."
      );
    } finally {
      setIsScanning(false);
    }
  };
    return (
    <motion.section
      className="scanner-page"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="scanner-heading">
        <div>
          <span className="scanner-eyebrow">THREAT INTELLIGENCE / SCANNER</span>
          <h1>Artifact Scanner</h1>
          <p>Inspect files for sensitive information and cross-artifact exposure.</p>
        </div>

        <div className="scanner-status">
          <span className="status-dot"></span>
          API CONNECTED
        </div>
      </div>

      <div
        className="scanner-dropzone"
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
        onClick={() => fileInput.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            fileInput.current?.click();
          }
        }}
      >
        <div className="scanner-upload-icon">
          <Upload size={30} />
        </div>

        <h2>Drop your artifacts here</h2>
        <p>or click to browse files from your computer</p>
        <span>PDF · TXT · CSV · JSON · PY · JS · JAVA · LOG</span>

        <input
          ref={fileInput}
          type="file"
          multiple
          accept=".pdf,.txt,.csv,.json,.py,.js,.java,.log"
          onChange={handleFileChange}
          hidden
        />
      </div>
            <div className="scanner-file-panel">
        <div className="scanner-panel-heading">
          <div>
            <h2>Selected artifacts</h2>
            <p>{selectedFiles.length} / 10 files selected</p>
          </div>

          {selectedFiles.length > 0 && (
            <button className="scanner-clear" onClick={clearFiles}>
              <Trash2 size={15} />
              Clear all
            </button>
          )}
        </div>

        {selectedFiles.length === 0 ? (
          <div className="scanner-empty">
            No artifacts selected yet.
          </div>
        ) : (
          selectedFiles.map((file, index) => (
            <div className="scanner-file-row" key={`${file.name}-${index}`}>
              <FileText size={20} />

              <div className="scanner-file-info">
                <strong>{file.name}</strong>
                <span>{(file.size / 1024).toFixed(1)} KB</span>
              </div>

              <button
                className="scanner-remove"
                onClick={() => removeFile(index)}
                aria-label={`Remove ${file.name}`}
              >
                <Trash2 size={17} />
              </button>
            </div>
          ))
        )}

        <button
          className="scanner-scan-button"
          onClick={handleScan}
          disabled={isScanning || selectedFiles.length === 0}
        >
          {isScanning ? (
            <>
              <LoaderCircle className="scanner-spin" size={19} />
              Analyzing artifacts...
            </>
          ) : (
            <>
              <ScanSearch size={19} />
              Start Security Scan
            </>
          )}
        </button>

        {error && (
          <div className="scanner-error">
            <AlertTriangle size={17} />
            {error}
          </div>
        )}
      </div>
            {results && (
        <div className="scanner-results">
          <h2>
            <ShieldCheck size={21} />
            Scan Results
          </h2>

          <div className="scanner-result-stats">
            <div>
              <span>Files scanned</span>
              <strong>{results.total_files}</strong>
            </div>

            <div>
              <span>Correlations found</span>
              <strong>{results.total_correlations}</strong>
            </div>

            <div>
              <span>Sensitive findings</span>
              <strong>
                {results.files.reduce(
                  (total, file) => total + file.sensitive_findings_count,
                  0
                )}
              </strong>
            </div>
          </div>

          {results.files.map((file) => (
            <div className="scanner-result-card" key={file.redacted_file_id}>
              <div className="scanner-result-title">
                <FileText size={19} />

                <div>
                  <strong>{file.filename}</strong>
                  <span>{file.status}</span>
                </div>

                <span className="scanner-finding-count">
                  {file.sensitive_findings_count} findings
                </span>
              </div>

              {file.findings.length > 0 ? (
                file.findings.map((finding, index) => (
                  <div
                    className="scanner-finding"
                    key={`${finding.type}-${finding.start}-${index}`}
                  >
                    <ShieldAlert size={15} />
                    <strong>{finding.type}</strong>
                    <span>{finding.masked_value}</span>
                  </div>
                ))
              ) : (
                <p className="scanner-no-findings">
                  No sensitive information detected.
                </p>
              )}

              <a
                className="scanner-download"
                href={`${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}${file.download_url}`}
              >
                <Download size={16} />
                Download redacted file
              </a>
            </div>
          ))}

          {results.cross_artifact_correlations?.length > 0 && (
            <div className="scanner-correlations">
              <h3>Cross-Artifact Correlations</h3>

              {results.cross_artifact_correlations.map((item, index) => (
                <div className="scanner-correlation" key={index}>
                  <ShieldAlert size={18} />

                  <div>
                    <strong>{item.risk_level || "DETECTED"} RISK</strong>
                    <p>
                      {item.matched_identity || "Related identity"} ·{" "}
                      {item.related_files?.length || 0} related files
                    </p>
                    <span>
                      Evidence: {item.evidence_types?.join(", ")}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </motion.section>
  );
}

export default FileScanner;
