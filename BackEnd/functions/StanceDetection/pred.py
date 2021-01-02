#Adapted from https://github.com/uclmr/fakenewschallenge/blob/master/pred.py
#Original credit - @jaminriedel 

from .util import FNCData,bow_train,pipeline_test,save_predictions
import random
import tensorflow as tf
import numpy as np
import sys
import csv



class PredictStance:

    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)


    r = random.Random()
    r.seed(123)
    lim_unigram = 5000
    target_size = 4
    hidden_size = 100
    l2_alpha = 0.00001

    file_train_instances = "StanceDetection/train_stances.csv"
    file_train_bodies = "StanceDetection/train_bodies.csv"
    file_test_instances = "StanceDetection/test_stances.csv"
    file_test_bodies = "StanceDetection/test_bodies.csv"
    base_dir='./'


    raw_train = FNCData(base_dir,file_train_instances, file_train_bodies)
    raw_test = FNCData(base_dir,file_test_instances, file_test_bodies)

    bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer = bow_train(raw_train, raw_test, lim_unigram=lim_unigram)

    def restore_model(self,model_num):
    
        # Define graph
        tf.reset_default_graph()
        test_set = pipeline_test(model_num,self.raw_test, self.bow_vectorizer, self.tfreq_vectorizer, self.tfidf_vectorizer)
        feature_size = len(test_set[0])

        # Create placeholders
        features_pl = tf.placeholder(tf.float32, [None, feature_size], 'features')
        stances_pl = tf.placeholder(tf.int64, [None], 'stances')
        keep_prob_pl = tf.placeholder(tf.float32)

        # Infer batch size
        batch_size = tf.shape(features_pl)[0]

        # Define multi-layer perceptron
        hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, self.hidden_size)), keep_prob=keep_prob_pl)
        logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer, self.target_size), keep_prob=keep_prob_pl)
        logits = tf.reshape(logits_flat, [batch_size, self.target_size])

        # Define L2 loss
        tf_vars = tf.trainable_variables()
        l2_loss = tf.add_n([tf.nn.l2_loss(v) for v in tf_vars if 'bias' not in v.name]) * self.l2_alpha

        # Define overall loss
        loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=stances_pl) + l2_loss)

        # Define prediction
        softmaxed_logits = tf.nn.softmax(logits)
        predict = softmaxed_logits

        with tf.Session() as sess:
                
            saver = tf.train.Saver()
            saver.restore(sess,self.base_dir+'StanceDetection/model/model%d/mymodel'%model_num)

            # Predict
            test_feed_dict = {features_pl: test_set, keep_prob_pl: 1.0}
            test_pred = sess.run(predict, feed_dict=test_feed_dict)

        return test_pred

    def getPredictions(self, scraped_data_keys):
        #Define the weight for different class if needed
        weight_pred_1=np.diag(np.ones(4))
        weight_pred_2=np.diag(np.ones(4))
        weight_pred_3=np.diag(np.ones(4))


        test_prediction1= self.restore_model(1)
        test_prediction2= self.restore_model(2)
        test_prediction3= self.restore_model(3)


        final_pred=np.matmul(test_prediction1,weight_pred_1)+np.matmul(test_prediction2,weight_pred_2)+np.matmul(test_prediction3,weight_pred_3)


        final_pred_index = np.argmax(final_pred,1)
        save_predictions(final_pred_index, scraped_data_keys)

if __name__ == "__main__":
    p = PredictStance()
