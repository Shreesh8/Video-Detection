import React, { useState } from "react";
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
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stepper,
  Step,
  StepLabel,
  StepContent,
} from "@mui/material";
import { CloudUpload as CloudUploadIcon } from "@mui/icons-material";
import axios from "axios";
import Logo from "./quantai_logo.png";

function Header({ onHowItWorksClick }) {
  return (
    <Box
      sx={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        px: 4,
        py: 2,
        position: "absolute",
        top: 0,
        left: 0,
        zIndex: 20,
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", gap: 0 }}>
        <Box
          sx={{
            background: "transparent",
            borderRadius: "50%",
            p: 2.2,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <img src={Logo} alt="Logo" style={{ height: 140, width: "auto" }} />
        </Box>
        <Typography
          variant="h4"
          sx={{
            color: "#fff",
            fontWeight: 700,
            ml: "1px",
            textShadow: "0 2px 8px #0008",
          }}
        >
          QuantAI
        </Typography>
      </Box>
      <Button
        variant="text"
        onClick={onHowItWorksClick}
        sx={{
          color: "#fff",
          fontWeight: 600,
          fontSize: 18,
          textTransform: "none",
          background: "rgba(0,0,0,0.15)",
          borderRadius: 2,
          px: 2,
        }}
      >
        How it works
      </Button>
    </Box>
  );
}

function HowItWorksModal({ open, onClose }) {
  const steps = [
    {
      label: "Upload Video",
      description:
        "Select and upload any video file from your device. The system supports common video formats like MP4, AVI, MOV, etc.",
    },
    {
      label: "AI Processing",
      description:
        "Our advanced AI model (YOLOv8) analyzes each frame of your video to detect objects, track their movements, and identify activities.",
    },
    {
      label: "Object Detection",
      description:
        "The system identifies various objects in your video including people, vehicles, animals, and common items with high accuracy.",
    },
    {
      label: "Activity Analysis",
      description:
        "Based on the detected objects and their movements, the AI determines what activities are happening in the video.",
    },
    {
      label: "Results Display",
      description:
        "View detailed results including object counts, confidence levels, and activity descriptions in an easy-to-understand format.",
    },
  ];

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          background: "linear-gradient(135deg, #181c2f 0%, #2d174c 100%)",
          color: "white",
          borderRadius: 3,
        },
      }}
    >
      <DialogTitle
        sx={{
          textAlign: "center",
          fontSize: "2rem",
          fontWeight: 700,
          color: "white",
          borderBottom: "1px solid rgba(255,255,255,0.2)",
        }}
      >
        How It Works
      </DialogTitle>
      <DialogContent sx={{ mt: 2 }}>
        <Box sx={{ mb: 4 }}>
          <Typography
            variant="h6"
            sx={{ mb: 2, color: "#6a5af9", fontWeight: 600 }}
          >
            Background Process
          </Typography>
          <Typography variant="body1" sx={{ mb: 2, lineHeight: 1.6 }}>
            Our system uses state-of-the-art computer vision technology powered
            by YOLOv8 (You Only Look Once), a real-time object detection model.
            The AI processes your video frame by frame, identifying objects,
            tracking their movements, and analyzing patterns to understand
            what's happening in the scene.
          </Typography>
          <Typography variant="body1" sx={{ lineHeight: 1.6 }}>
            The system can detect various objects including people, vehicles,
            animals, and everyday items, providing you with detailed insights
            about the content and activities in your videos.
          </Typography>
        </Box>

        <Divider sx={{ my: 3, borderColor: "rgba(255,255,255,0.2)" }} />

        <Typography
          variant="h6"
          sx={{ mb: 3, color: "#f857a6", fontWeight: 600 }}
        >
          How to Use
        </Typography>

        <Stepper
          orientation="vertical"
          sx={{ "& .MuiStepLabel-root": { color: "white" } }}
        >
          {steps.map((step, index) => (
            <Step key={step.label} active={true}>
              <StepLabel>
                <Typography
                  variant="h6"
                  sx={{ color: "white", fontWeight: 600 }}
                >
                  {step.label}
                </Typography>
              </StepLabel>
              <StepContent>
                <Typography
                  variant="body1"
                  sx={{
                    color: "rgba(255,255,255,0.9)",
                    lineHeight: 1.6,
                    mb: 2,
                  }}
                >
                  {step.description}
                </Typography>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </DialogContent>
      <DialogActions sx={{ p: 3, pt: 0 }}>
        <Button
          onClick={onClose}
          variant="contained"
          sx={{
            background: "linear-gradient(90deg, #6a5af9 0%, #f857a6 100%)",
            color: "white",
            px: 4,
            py: 1.5,
            borderRadius: 2,
            fontWeight: 600,
            textTransform: "none",
          }}
        >
          Got it!
        </Button>
      </DialogActions>
    </Dialog>
  );
}

function WelcomePage({ onGetStarted }) {
  const [howItWorksOpen, setHowItWorksOpen] = useState(false);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100vw",
        background: "linear-gradient(135deg, #181c2f 0%, #2d174c 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
      }}
    >
      <Header onHowItWorksClick={() => setHowItWorksOpen(true)} />
      <HowItWorksModal
        open={howItWorksOpen}
        onClose={() => setHowItWorksOpen(false)}
      />
      {/* Centered content */}
      <Box sx={{ textAlign: "center", zIndex: 10 }}>
        <Typography
          variant="h2"
          sx={{
            color: "white",
            fontWeight: 800,
            mb: 2,
            textShadow: "0 4px 32px #000",
          }}
        >
          Video Object Detection
        </Typography>
        <Typography
          variant="h5"
          sx={{ color: "white", mb: 4, textShadow: "0 2px 16px #000" }}
        >
          Analyze videos, track objects, and visualize movement with AI.
        </Typography>
        <Button
          variant="contained"
          sx={{
            px: 5,
            py: 1.5,
            fontSize: 22,
            fontWeight: 700,
            background: "linear-gradient(90deg, #6a5af9 0%, #f857a6 100%)",
            color: "#fff",
            borderRadius: 3,
            boxShadow: "0 4px 32px #0008",
            textTransform: "none",
          }}
          onClick={onGetStarted}
        >
          Get Started
        </Button>
      </Box>
    </Box>
  );
}

function App() {
  const [showWelcome, setShowWelcome] = useState(true);
  const [howItWorksOpen, setHowItWorksOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [detections, setDetections] = useState(null);
  const [activity, setActivity] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [processingStats, setProcessingStats] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type.startsWith("video/")) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please select a valid video file");
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError(null);
    setDetections(null);
    setActivity(null);
    setProcessingStats(null);

    try {
      const response = await axios.post(
        "http://localhost:8001/predict",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setDetections(response.data.detections);
      setActivity(response.data.activity);
      setProcessingStats({
        framesProcessed: response.data.frames_processed,
        totalObjects: response.data.total_objects_detected,
      });
      console.log(
        "API response - Detections:",
        response.data.detections,
        "Activity:",
        response.data.activity
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "An error occurred while processing the video"
      );
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return "success";
    if (confidence >= 0.6) return "warning";
    return "error";
  };

  // Debug log for state
  console.log("Detections:", detections, "Activity:", activity);

  if (showWelcome) {
    return <WelcomePage onGetStarted={() => setShowWelcome(false)} />;
  }

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100vw",
        background: "linear-gradient(135deg, #181c2f 0%, #2d174c 100%)",
        position: "relative",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Header onHowItWorksClick={() => setHowItWorksOpen(true)} />
      <HowItWorksModal
        open={howItWorksOpen}
        onClose={() => setHowItWorksOpen(false)}
      />
      <Container maxWidth="sm" sx={{ p: 0 }}>
        <Paper
          elevation={6}
          sx={{
            p: { xs: 2, sm: 4 },
            pt: { xs: 3, sm: 5 },
            pb: { xs: 3, sm: 5 },
            mt: 0,
            borderRadius: 4,
            background: "rgba(255,255,255,0.85)",
            boxShadow: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            minWidth: { xs: "90vw", sm: 400 },
            maxWidth: 500,
          }}
        >
          <Typography
            variant="h4"
            component="h1"
            gutterBottom
            align="center"
            sx={{ fontWeight: 700, mb: 3, color: "#222" }}
          >
            Video Object Detection
          </Typography>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 2,
              width: "100%",
            }}
          >
            <input
              accept="video/*"
              style={{ display: "none" }}
              id="video-upload"
              type="file"
              onChange={handleFileChange}
            />
            <label htmlFor="video-upload">
              <Button
                variant="contained"
                component="span"
                startIcon={<CloudUploadIcon />}
                sx={{ fontWeight: 600, letterSpacing: 1 }}
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
              sx={{ mt: 2, width: "100%" }}
            >
              {loading ? <CircularProgress size={24} /> : "Analyze Video"}
            </Button>
            {error && (
              <Alert severity="error" sx={{ mt: 2, width: "100%" }}>
                {error}
              </Alert>
            )}
            {/* Always show activity above detections if present */}
            {activity && (
              <Alert severity="info" sx={{ mt: 2, width: "100%" }}>
                Activity: {activity}
              </Alert>
            )}
            {detections && (
              <Box sx={{ mt: 3, width: "100%" }}>
                <Typography variant="h6" gutterBottom>
                  Detection Results
                </Typography>
                {/* Show processing stats */}
                {processingStats && (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mb: 2 }}
                  >
                    Processed {processingStats.framesProcessed} frames • Total
                    objects detected: {processingStats.totalObjects}
                  </Typography>
                )}
                <Grid container spacing={2}>
                  {detections.map((detection, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6" component="div" gutterBottom>
                            {detection.class}
                          </Typography>
                          <Box
                            sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}
                          >
                            <Chip
                              label={`Count: ${detection.count}`}
                              color="primary"
                              variant="outlined"
                            />
                            <Chip
                              label={`Confidence: ${(
                                detection.confidence * 100
                              ).toFixed(1)}%`}
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
      </Container>
    </Box>
  );
}

export default App;
