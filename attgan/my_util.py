from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from functools import partial
import json
import traceback


import attgan.imlib as im
import numpy as np
import attgan.pylib as pylib
import tensorflow as tf
import attgan.tflib as tl
import attgan.my_data_deal as my_data_deal

import attgan.models as models

global sess
# ==============================================================================
# =                                    param                                   =
# ==============================================================================



def get_result(input_data,test_atts=None,test_ints=None):
    global sess
    parser = argparse.ArgumentParser()
    args_ = parser.parse_args()
    with open('./attgan/output/128_shortcut1_inject1_none/setting.txt') as f:
        args = json.load(f)

    # model
    atts = args['atts']
    n_att = len(atts)
    img_size = args['img_size']
    shortcut_layers = args['shortcut_layers']
    inject_layers = args['inject_layers']
    enc_dim = args['enc_dim']
    dec_dim = args['dec_dim']
    dis_dim = args['dis_dim']
    dis_fc_dim = args['dis_fc_dim']
    enc_layers = args['enc_layers']
    dec_layers = args['dec_layers']
    dis_layers = args['dis_layers']
    # testing

    thres_int = args['thres_int']

    # others

    experiment_name = args["experiment_name"]

 #   assert test_atts is not None, 'test_atts should be chosen in %s' % (str(atts))
 #    for a in test_atts:
 #
 #        assert a in atts, 'test_atts should be chosen in %s' % (str(atts))

  #  assert len(test_ints) == len(test_atts), 'the lengths of test_ints and test_atts should be the same!'


    # ==============================================================================
    # =                                   graphs                                   =
    # ==============================================================================

    # data

    sess = tl.session()
    te_data = my_data_deal.Celeba(input_data, atts, img_size, 1, sess = sess, crop=True)
    # models
    Genc = partial(models.Genc, dim=enc_dim, n_layers=enc_layers)
    Gdec = partial(models.Gdec, dim=dec_dim, n_layers=dec_layers, shortcut_layers=shortcut_layers, inject_layers=inject_layers)
    D = partial(models.D, n_att=n_att, dim=dis_dim, fc_dim=dis_fc_dim, n_layers=dis_layers)


    # inputs
    xa_sample = tf.placeholder(tf.float32, shape=[None, img_size, img_size, 3])
    _b_sample = tf.placeholder(tf.float32, shape=[None, n_att])

    # sample
    x_sample = Gdec(Genc(xa_sample, is_training=False), _b_sample, is_training=False)

    xa_logit_gan, xa_logit_att = D(xa_sample)  ###xa_logit_attr b_

    # ==============================================================================
    # =                                    test                                    =
    # ==============================================================================

    # # initialization


    ckpt_dir = './attgan/output/%s/checkpoints' % experiment_name
    try:
        tl.load_checkpoint(ckpt_dir, sess)
    except:
        raise Exception(' [*] No checkpoint!')

    try:
        batch = te_data.get_next()

        data1 = batch[0]  # 10 128 128 3
        xa_sample_ipt = data1.reshape([1, 128, 128, 3])
        a_sample_ipt = sess.run(xa_logit_att, feed_dict={xa_sample: xa_sample_ipt}) > 0
        b_sample_ipt = np.array(a_sample_ipt, copy=True).astype(np.int)

        if test_atts == None:
            return b_sample_ipt

        for a in test_atts:
            i = atts.index(a)
            b_sample_ipt[:, i] = 1 - b_sample_ipt[:, i]   # inverse attribute
            b_sample_ipt = my_data_deal.Celeba.check_attribute_conflict(b_sample_ipt, atts[i], atts)

        x_sample_opt_list = [xa_sample_ipt, np.full((1, img_size, img_size // 10, 3), -1.0)]
        _b_sample_ipt = (b_sample_ipt * 2 - 1) * thres_int
        for a, i in zip(test_atts, test_ints):
            _b_sample_ipt[..., atts.index(a)] = _b_sample_ipt[..., atts.index(a)] * i / thres_int
        x_sample_opt_list.append(sess.run(x_sample, feed_dict={xa_sample: xa_sample_ipt, _b_sample: _b_sample_ipt}))
        sample = np.concatenate(x_sample_opt_list, 2)

        save_dir = './attgan/output/%s/sample_testing_multi_%s' % (experiment_name, str(test_atts))
        pylib.mkdir(save_dir)
        term = sample.squeeze(0)
        im.imwrite(term, '%s/%d.png' % (save_dir, 1))

        print('%d.png done!' % (1))





    except:
        traceback.print_exc()
    finally:
        sess.close()



# input_data = "../train/000001.jpg"
#
# get_result(input_data, test_atts=["Pale_Skin"],test_ints=[0.1])