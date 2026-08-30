const API_URL = "http://localhost:8000";

export default async function getdata() {
  const response = await fetch(`${API_URL}/data`);
  if (!response.ok) throw new Error("Erreur lors du chargement des données");
  const data = response.json();
  return data;
}

export async function askQuestion(question) {
  try {
    const response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error asking question:", error);
    throw error;
  }
}

export async function importFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/import/file`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Import fichier échoué");
  return response.json();
}

export async function generatefile() {
  const response = await fetch(`${API_URL}/generatefile`, { method: "GET" });
  if (!response.ok) throw new Error("Génération automatique fichier échoué");
  return response.json();
}