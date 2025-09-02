// worker.js
// Este script roda em uma thread separada para não travar a UI principal.
// Ele lida com a requisição da API e o processamento da resposta.

onmessage = async (e) => {
    // A API do Render.com. Substitua pela sua URL real e adicione o endpoint /convert.
    const API_URL = 'https://texconversor.onrender.com/convert';
    
    // Recebe os dados do arquivo do script principal
    const file = e.data;

    if (!file) {
        postMessage({ error: "Nenhum arquivo recebido." });
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            // Se a resposta não for OK, lemos como texto para obter a mensagem de erro
            const errorMessage = await response.text();
            throw new Error(`Erro da API: ${response.status} - ${errorMessage}`);
        }

        // Se a resposta for um sucesso, lemos como um Blob (arquivo)
        const blob = await response.blob();
        
        // Enviamos o Blob de volta para a UI principal para iniciar o download
        postMessage({ blob: blob });

    } catch (error) {
        // Em caso de erro, enviamos a mensagem para a UI principal
        postMessage({ error: error.message });
    }
};
