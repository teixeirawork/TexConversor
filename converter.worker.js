self.onmessage = async function(event) {
    const file = event.data.file;
    const fileName = event.data.fileName;

    const formData = new FormData();
    formData.append('pdf_file', file);

    const API_URL = 'https://texconversor.onrender.com'; // Substitua por sua URL real do Render.com

    try {
        self.postMessage({ type: 'progress', payload: { progress: 50 } });

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        // Verifica se a resposta da API foi bem-sucedida
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erro da API: ${response.status} - ${errorText}`);
        }

        const docxBlob = await response.blob();
        
        self.postMessage({
            type: 'success',
            payload: {
                data: docxBlob,
                fileName: fileName.replace('.pdf', '.docx')
            }
        });
        
    } catch (error) {
        console.error('Erro na conversão:', error);
        self.postMessage({
            type: 'error',
            payload: { error: error.message }
        });
    }
};
