import { useState } from "react";
import "../css/Header.css";
import { generatefile } from "../router";
import DataImport from "./DataImport";
import { TEXT } from "../constants/text";

export default function Header({ onImported }) {
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState("");

  async function handleGenerate() {
    setGenerating(true);
    setGenError("");
    try {
      const response = await generatefile();
      await onImported(response);
    } catch (err) {
      setGenError(TEXT.header.generateError);
    } finally {
      setGenerating(false);
    }
  }

  return (
    <header className="header">
      {/* Bandeau "predylics" qui défile en boucle, purement décoratif */}
      <div className="header__marquee" aria-hidden="true">
        <div className="header__marquee-track">
          {Array.from({ length: 12 }).map((_, i) => (
            <span key={i} className="header__marquee-item">
              {TEXT.header.marqueeLabel}
            </span>
          ))}
        </div>
      </div>

      <div className="header__content">
        <div className="header__brand">
          <span className="header__logo">
            {TEXT.header.brandName}
            <span className="header__logo-accent">{TEXT.header.brandAccent}</span>
          </span>
          <span className="header__subtitle">{TEXT.header.subtitle}</span>
        </div>

        <div className="header__actions">
          <DataImport onImported={onImported} />

          <button className="header__generate-btn" onClick={handleGenerate} disabled={generating}>
            {TEXT.header.generateBtnIcon} {generating ? TEXT.header.generateBtnLoading : TEXT.header.generateBtnIdle}
          </button>

          {genError && <span className="header__error">{genError}</span>}
        </div>
      </div>
    </header>
  );
}
