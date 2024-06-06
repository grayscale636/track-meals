# Food Detection Machine Learning Model Readme

## Overview

This repository contains a machine learning model for food detection using transfer learning using MobileNetV2 and converted into TFLite. The model is designed to identify and detect types of food items. The project also utilizes OS module for file system operations, Tensorflow for transfer learning, anf Tensorand for monitoring the training.

## Technologies Used

1. **TensorFlow**: An open-source machine learning framework developed by the TensorFlow team at Google.

2. **Keras**: A high-level neural networks API, written in Python and capable of running on top of TensorFlow.

3. **Matplotlib**: A 2D plotting library for Python, used for creating static, animated, and interactive visualizations.

4. **OS module**: A Python module that provides a way to interact with the operating system, allowing file system operations.

## Steps to Replicate

### Prerequisites

Before you begin, ensure you have the following installed:

- Python: [Download and Install Python](https://www.python.org/downloads/)

### Clone the Repository

```bash
git clone https://github.com/CH2-PS338/model-food-detection.git
```

### Install Dependencies

This project using pretrained model in tensorflow model zoo:

```bash
(https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
```

### Data Preparation

Prepare your dataset and place it in the designated data directory.

### Pretrained model

This link to pretrained model:

```bash[
http://download.tensorflow.org/models/object_detection/tf2
```

### Evaluate the Model

Evaluate the performance of the trained model using mAP:

```bash
calculate_map_cartucho.py
```

### Make Predictions

Use the trained model to make predictions:

```bash
python make_predictions.py
```

### Convert to TFLite

Convert to TFLite using TFLite Converter

```bash
converter = tf.lite.TFLiteConverter.from_saved_model('/content/custom_model_lite/saved_model')
tflite_model = converter.convert()
```
