import tensorflow as tf
from tensorflow.python.keras import ResNet50
from tensorflow.python.keras import layers, Model

""" Image Encoder: Use a pre-trained CNN like ResNet50 to encode the crochet photo into a feature vector.
Text Decoder: Use an LSTM or Transformer-based model to generate instructions from the image features.
Training: Train the combined model on paired image-instruction data.
Inference: Given a new photo, the model predicts the corresponding crochet instructions.
This workflow leverages the power of pre-trained models to handle the complexity of visual data, making it more feasible to train the system even with a relatively small dataset."""


def build_image_encoder():
    # Load pre-trained ResNet50 model + higher level layers
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Add a global spatial average pooling layer
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    
    # Add a fully-connected layer and a final layer to generate image features
    x = layers.Dense(256, activation='relu')(x)
    image_features = layers.Dense(128, activation='relu')(x)
    
    encoder_model = Model(inputs=base_model.input, outputs=image_features)
    return encoder_model

def build_text_decoder(vocab_size, max_length):
    # The input for the text sequence
    text_input = layers.Input(shape=(max_length,))
    
    # The image features from the encoder
    image_features_input = layers.Input(shape=(128,))
    
    # Embedding layer for text
    x = layers.Embedding(input_dim=vocab_size, output_dim=128)(text_input)
    
    # LSTM to generate the sequence
    x = layers.LSTM(256, return_sequences=True)(x)
    x = layers.LSTM(256)(x)
    
    # Combine image features with the LSTM output
    combined = layers.concatenate([x, image_features_input])
    
    # Final dense layers to produce the vocabulary output
    x = layers.Dense(256, activation='relu')(combined)
    output = layers.Dense(vocab_size, activation='softmax')(x)
    
    decoder_model = Model(inputs=[text_input, image_features_input], outputs=output)
    return decoder_model

def build_image_to_text_model(encoder, decoder, max_length):
    # Inputs
    image_input = encoder.input
    text_input = decoder.input[0]
    
    # Image features from the encoder
    image_features = encoder.output
    
    # Output from the decoder
    output = decoder([text_input, image_features])
    
    # Combined model
    model = Model(inputs=[image_input, text_input], outputs=output)
    return model

# Example setup
vocab_size = 5000  # Example vocabulary size
max_length = 100   # Maximum length of the instruction sequence

# Build the encoder, decoder, and full model
encoder = build_image_encoder()
decoder = build_text_decoder(vocab_size, max_length)
model = build_image_to_text_model(encoder, decoder, max_length)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

# Assuming X_images are your image inputs and Y_sequences are your tokenized instructions
# Y_sequences_input should be the input sequences and Y_sequences_output should be the target sequences (shifted by one position)

# Example code to train the model
model.fit([X_images, Y_sequences_input], Y_sequences_output, epochs=10, batch_size=32)

def predict_instructions(encoder, decoder, image, max_length, tokenizer):
    # Encode the image into features
    image_features = encoder.predict(image)
    
    # Start with the start token
    start_seq = tokenizer.texts_to_sequences(['<start>'])[0]
    seq = start_seq
    
    # Generate words one by one
    for i in range(max_length):
        seq_input = pad_sequences([seq], maxlen=max_length, padding='post')
        y_pred = decoder.predict([seq_input, image_features])
        y_pred = tf.argmax(y_pred, axis=-1).numpy()[0]
        
        word = tokenizer.index_word[y_pred[-1]]
        seq.append(y_pred[-1])
        
        if word == '<end>':  # Stop when the end token is generated
            break
    
    return ' '.join([tokenizer.index_word[idx] for idx in seq if idx > 0])

# Example usage
predicted_instructions = predict_instructions(encoder, decoder, image, max_length, tokenizer)
print(predicted_instructions)
