from lib import inception_resnet_v1 as resnet
import numpy as np
import tensorflow as tf

class face_feture_reg(object):
	"""docstring for face_feture_reg"""
	def __init__(self, face_rec,model_path = 'models/model-20170512-110547.ckpt-250000'):
		with face_rec.graph.as_default():
			self.sess = tf.Session()
			self.x = tf.placeholder('float', [None,160,160,3])
			self.inside_resnet = tf.nn.l2_normalize( resnet.inference(self.x, 0.6,phase_train=False)[0], 1, 1e-10)
			saver = tf.train.Saver()
			saver.restore(self.sess, model_path)

	def get_features(self, imgs):
	 	#resize and add whiten
	 	imgs_local = np.zeros((len(imgs), 160, 160, 3))
	 	i = 0 
	 	for img  in imgs:
	 		if img is not None:
	 			#whiten
	 			mean = np.mean(img)
	 			std = np.std(img)
	 			std_revise = np.maximum(std, 1.0/np.sqrt(img.size))
	 			whiten_img = np.multiply(np.subtract(img, mean), 1/std_revise)
	 			imgs_local[i, :, :, :] = whiten_img
	 			i += 1
	 	return self.sess.run(self.inside_resnet, feed_dict = {self.x : imgs_local})

