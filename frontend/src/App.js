import React, { useState } from 'react';
import {
    Container,
    Box,
    Typography,
    Button,
    Paper,
    CircularProgress,
    Alert,
    List,
    ListItem,
    ListItemText,
    Chip,
    Divider,
    Card,
    CardContent,
    Grid
} from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import axios from 'axios';

function App() {
    const [file, setFile] = useState(null);
    const [detections, setDetections] = useState(null);
    const [activity, setActivity] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && selectedFile.type.startsWith('video/')) {
            setFile(selectedFile);
            setError(null);
        } else {
            setError('Please select a valid video file');
            setFile(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        setError(null);
        setDetections(null);
        setActivity(null);

        try {
            // Use environment variable for backend URL
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            if (!backendUrl) {
                throw new Error("Backend URL not configured. Please set REACT_APP_BACKEND_URL environment variable.");
            }
            const response = await axios.post(`${backendUrl}/predict`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setDetections(response.data.detections);
            setActivity(response.data.activity);
            console.log('API response - Detections:', response.data.detections, 'Activity:', response.data.activity);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred while processing the video');
        } finally {
            setLoading(false);
        }
    };

    const getConfidenceColor = (confidence) => {
        if (confidence >= 0.8) return 'success';
        if (confidence >= 0.6) return 'warning';
        return 'error';
    };

    // Debug log for state
    console.log('Detections:', detections, 'Activity:', activity);

    return (
        <Container maxWidth="md">
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom align="center">
                    Video Object Detection
                </Typography>

                <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                        <input
                            accept="video/*"
                            style={{ display: 'none' }}
                            id="video-upload"
                            type="file"
                            onChange={handleFileChange}
                        />
                        <label htmlFor="video-upload">
                            <Button
                                variant="contained"
                                component="span"
                                startIcon={<CloudUploadIcon />}
                            >
                                Select Video
                            </Button>
                        </label>

                        {file && (
                            <Typography variant="body2" color="text.secondary">
                                Selected: {file.name}
                            </Typography>
                        )}

                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleUpload}
                            disabled={!file || loading}
                            sx={{ mt: 2 }}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Analyze Video'}
                        </Button>

                        {error && (
                            <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
                                {error}
                            </Alert>
                        )}

                        {/* Always show activity above detections if present */}
                        {activity && (
                            <Alert severity="info" sx={{ mt: 2, width: '100%' }}>
                                Activity: {activity}
                            </Alert>
                        )}

                        {detections && (
                            <Box sx={{ mt: 3, width: '100%' }}>
                                <Typography variant="h6" gutterBottom>
                                    Detection Results
                                </Typography>
                                <Grid container spacing={2}>
                                    {detections.map((detection, index) => (
                                        <Grid item xs={12} sm={6} md={4} key={index}>
                                            <Card>
                                                <CardContent>
                                                    <Typography variant="h6" component="div" gutterBottom>
                                                        {detection.class}
                                                    </Typography>
                                                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                                        <Chip
                                                            label={`Count: ${detection.count}`}
                                                            color="primary"
                                                            variant="outlined"
                                                        />
                                                        <Chip
                                                            label={`Confidence: ${(detection.confidence * 100).toFixed(1)}%`}
                                                            color={getConfidenceColor(detection.confidence)}
                                                            variant="outlined"
                                                        />
                                                    </Box>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                    ))}
                                </Grid>
                            </Box>
                        )}
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
}

export default App; 