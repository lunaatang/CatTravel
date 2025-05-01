import { useState } from 'react'
import axios, { AxiosError } from 'axios'
import './App.css'

interface ApiError {
  detail: string;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [location, setLocation] = useState('')
  const [resultImage, setResultImage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0]
      const fileExt = file.name.split('.').pop()?.toLowerCase()
      if (fileExt && !['jpg', 'jpeg', 'png'].includes(fileExt)) {
        setError('Only JPG, JPEG, and PNG formats are supported')
        setSelectedFile(null)
        return
      }
      setSelectedFile(file)
      setError(null)
    }
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!selectedFile || !location) {
      setError('Please select an image and enter a location')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', selectedFile)
    formData.append('location', location)

    try {
      const response = await axios.post('http://localhost:8000/process-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResultImage(response.data.image_url)
    } catch (err) {
      const error = err as AxiosError<ApiError>
      setError(error.response?.data?.detail || 'Error processing image. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Cat Travel</h1>
      <p>Upload a cat photo and choose a destination!</p>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="input-group">
          <label htmlFor="file-input" className="file-label">
            Choose an image (JPG, JPEG, PNG supported)
          </label>
          <input
            id="file-input"
            type="file"
            accept="image/jpeg,image/png"
            onChange={handleFileChange}
            className="file-input"
          />
          {selectedFile && (
            <div className="file-info">
              Selected: {selectedFile.name}
            </div>
          )}
        </div>
        
        <div className="input-group">
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter a location (e.g., Paris, the moon)"
            className="location-input"
          />
      </div>
        
        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Processing...' : 'Generate'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {resultImage && (
        <div className="result">
          <h2>Your Cat's New Adventure</h2>
          <div className="image-container">
            <img src={resultImage} alt="Generated cat travel image" className="result-image" />
          </div>
        </div>
      )}
      </div>
  )
}

export default App
