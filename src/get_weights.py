import tensorflow as tf
import spinup
import sys
from tensorflow.python.platform import gfile
from google.protobuf import text_format


with tf.Session(graph=tf.Graph()) as sess:
#    with gfile.FastGFile("output_dir2/simple_save/saved_model.pb", 'rb') as f:
#        proto_b = f.read()
#        graph_def = tf.GraphDef()
#        text_format.Merge(proto_b, graph_def) 
#
#        graph_def.ParseFromString(proto_b)
#        sess.graph.as_default()
#        tf.import_graph_def(graph_def, name='')
#        constant_ops = [op for op in sess.graph.get_operations() if op.type == "Const"]
#        for constant_op in constant_ops:
#            value =  sess.run(constant_op.outputs[0])
#            constant_values[constant_op.name] = value
#            print(constant_ops.name, value)

#    tf.saved_model.loader.load(sess, ["v"], "output_dir2/simple_save/")
    tensors = spinup.utils.logx.restore_tf_graph(sess, "output_dir2/simple_save/")

    ops = tensors['v'].graph.get_operations()
    for op in ops:
        try:
            w = sess.run(op.outputs[0])
            print(w, op.name)
        except:
            w = 0
