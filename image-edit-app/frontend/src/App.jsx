import { useState } from 'react';
import './index.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [editedImageUrl, setEditedImageUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    setSelectedFile(file ?? null);
    setError('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      setError('Please upload an image to edit.');
      return;
    }
    if (!prompt.trim()) {
      setError('Please provide instructions for editing.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('prompt', prompt);

    try {
      setIsSubmitting(true);
      setError('');
      const response = await fetch('/api/edit', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const message = (await response.json())?.detail || 'Failed to edit image.';
        throw new Error(message);
      }

      const data = await response.json();
      setEditedImageUrl(data.edited_image_url);
    } catch (err) {
      setError(err.message || 'Something went wrong while editing the image.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1 className="title">Image Editor</h1>
        <div className="columns">
          <form className="left" onSubmit={handleSubmit}>
            <label className="section-label">1. Upload your image</label>
            <label className="upload-area" htmlFor="upload-input">
              <div>
                <div className="upload-icon">📷</div>
                <p className="upload-text">Click to browse or drag and drop</p>
                {selectedFile ? (
                  <p className="file-name">Selected: {selectedFile.name}</p>
                ) : (
                  <p className="helper-text">PNG or JPG, up to ~5MB</p>
                )}
              </div>
              <input
                id="upload-input"
                type="file"
                accept="image/png,image/jpeg"
                onChange={handleFileChange}
                className="upload-input"
              />
            </label>

            <label className="section-label" htmlFor="prompt-input">
              2. Describe your edits
            </label>
            <textarea
              id="prompt-input"
              className="prompt"
              placeholder="Example: Replace the background with a beach at sunset."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
            />

            {error && <p className="error">{error}</p>}
            <button className="submit" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Editing...' : 'Submit'}
            </button>
          </form>

          <div className="right">
            <div className="preview-frame">
              {editedImageUrl ? (
                <img src={editedImageUrl} alt="Edited result" className="preview-image" />
              ) : (
                <p className="placeholder">Your edited image will appear here</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
