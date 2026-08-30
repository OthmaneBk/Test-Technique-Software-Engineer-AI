// Module centralisant tous les textes affichés dans l'application.
// Chaque page/composant importe ces variables au lieu d'écrire du texte en dur.

export const TEXT = {
  app: {
    loadError: "Erreur chargement des données :",
  },
  header: {
    brandName: "predylics",
    brandAccent: ">",
    subtitle: "Analyse de données",
    marqueeLabel: "predylics>",
    generateBtnIcon: "✨",
    generateBtnIdle: "Générer un dataset automatique",
    generateBtnLoading: "Génération...",
    generateError: "Échec de la génération d'une nouvelle dataset.",
  },
  dataImport: {
    fileButton: "Importer un fichier CSV",
    importing: "Import en cours...",
    importError: "Échec de l'import du fichier.",
  },
  dataTable: {
    title: "📊 Données",
    countSuffix: "lignes",
    empty: "Aucune donnée à afficher pour le moment.",
  },
  chatAssistant: {
    heading: "Assistant IA",
    agentEmoji: "🤖",
    emptyState: "👋 Posez une question sur vos données pour commencer.",
    showAllDataAnswer: "Voici l'ensemble des données, affichées dans le tableau à gauche.",
    askError: "Erreur lors de l'appel à l'assistant.",
    inputPlaceholder: "Pose une question sur les données...",
    sendIcon: "➤",
  },
};
