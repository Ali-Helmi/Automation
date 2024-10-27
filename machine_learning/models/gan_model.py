# machine_learning/models/gan_model.py
import tensorflow as tf
from tensorflow.keras import layers

class GAN:
    def __init__(self, input_dim, noise_dim=100):
        self.noise_dim = noise_dim
        self.generator = self.build_generator(input_dim)
        self.discriminator = self.build_discriminator(input_dim)
        self.gan_model = self.build_gan()

    def build_generator(self, input_dim):
        model = tf.keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(self.noise_dim,)),
            layers.Dense(256, activation='relu'),
            layers.Dense(input_dim, activation='sigmoid')
        ])
        return model

    def build_discriminator(self, input_dim):
        model = tf.keras.Sequential([
            layers.Dense(256, activation='relu', input_shape=(input_dim,)),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def build_gan(self):
        self.discriminator.trainable = False
        model = tf.keras.Sequential([self.generator, self.discriminator])
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model

    def train(self, data, epochs=10000, batch_size=32):
        for epoch in range(epochs):
            noise = tf.random.normal([batch_size, self.noise_dim])
            generated_data = self.generator(noise)

            real_data = data.sample(batch_size)
            x_combined = tf.concat([generated_data, real_data], axis=0)
            y_combined = tf.concat([tf.zeros((batch_size, 1)), tf.ones((batch_size, 1))], axis=0)

            d_loss = self.discriminator.train_on_batch(x_combined, y_combined)

            noise = tf.random.normal([batch_size, self.noise_dim])
            y_gan = tf.ones((batch_size, 1))
            g_loss = self.gan_model.train_on_batch(noise, y_gan)

            if epoch % 1000 == 0:
                print(f"Epoch {epoch} - Discriminator Loss: {d_loss:.4f}, Generator Loss: {g_loss:.4f}")
