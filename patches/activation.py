import tensorflow as tf


def dice(_x, axis=-1, epsilon=1e-09, name=""):
    with tf.variable_scope(name, reuse=tf.AUTO_REUSE):
        alphas = tf.get_variable("alpha" + name, _x.get_shape()[-1], initializer=tf.constant_initializer(0.0), dtype=tf.float32)
        input_shape = list(_x.get_shape())

        reduction_axes = list(range(len(input_shape)))
        del reduction_axes[axis]
        broadcast_shape = [1] * len(input_shape)
        broadcast_shape[axis] = input_shape[axis]

    mean = tf.reduce_mean(_x, axis=reduction_axes)
    brodcast_mean = tf.reshape(mean, broadcast_shape)
    std = tf.reduce_mean(tf.square(_x - brodcast_mean) + epsilon, axis=reduction_axes)
    std = tf.sqrt(std)
    brodcast_std = tf.reshape(std, broadcast_shape)
    x_normed = (_x - brodcast_mean) / (brodcast_std + epsilon)
    x_p = tf.sigmoid(x_normed)

    return alphas * (1.0 - x_p) * _x + x_p * _x


def prelu(_x, scope=""):
    with tf.name_scope(name=scope):
        # _alpha = tf.get_variable(
        #     "prelu_" + scope, shape=_x.get_shape()[-1], dtype=_x.dtype, initializer=tf.constant_initializer(0.1)
        # )
        _alpha = tf.Variable(
            initial_value=tf.constant(0.1, shape=_x.shape[-1:]),
            name="prelu_" + scope,
            dtype=_x.dtype
        )
        return tf.maximum(0.0, _x) + _alpha * tf.minimum(0.0, _x)
