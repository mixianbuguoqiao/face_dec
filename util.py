import cv2


from functools import partial
import json


import attgan.imlib as im
import numpy as np

import tensorflow as tf
import attgan.tflib as tl
import attgan.my_data_deal as my_data_deal

import attgan.models as models

from importlib import import_module
Camera = import_module('camera.camera_' + "opencv").Camera

# global sess
# sess = None
#sess = tl.session()
args = json.load(open('./attgan/output/128_shortcut1_inject1_none/setting.txt'))
sess = None
def gen(camera):
    """Video streaming generator function."""
    facecasc = cv2.CascadeClassifier('./static/haarcascade_files/haarcascade_frontalface_default.xml')

    while True:
        frame = camera.get_frame()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = facecasc.detectMultiScale(gray, 1.3, 5)
        if not len(faces) > 0:
           pass
        else:
            for face in faces:

                (x, y, w, h) = face

                middle_x = int(x + (w / 2))
                middle_y = int(y + (h / 2))


                if y + h - 5 > y + 10 and x + w - 10 > x + 10:
                    cropImg = frame[middle_y - 163: middle_y + 164 , middle_x - 133 : middle_x + 134]
                    cv2.imwrite("123.jpg",cropImg)
                else:
                    continue

                frame = cv2.rectangle(frame, (middle_x - 133, middle_y - 163), (middle_x + 134, middle_y + 164 ), (255, 0, 0), 2)


        frame = cv2.imencode('.jpg', frame)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



def get_result(input_data,test_atts=None,test_ints=None):
    global sess

    # with open('./attgan/output/128_shortcut1_inject1_none/setting.txt') as f:
    #     args = json.load(f)

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

    # ==============================================================================
    # =                                   graphs                                   =
    # ==============================================================================

    # data


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
    print("------------",sess)
    if sess == None:

        sess = tl.session()

        ckpt_dir = './attgan/output/%s/checkpoints' % experiment_name

        tl.load_checkpoint(ckpt_dir, sess)

        te_data = my_data_deal.Celeba(input_data, atts, img_size, 1, sess=sess, crop=True)
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

        _b_sample_ipt = (b_sample_ipt * 2 - 1) * thres_int

        for a, i in zip(test_atts, test_ints):
            _b_sample_ipt[..., atts.index(a)] = _b_sample_ipt[..., atts.index(a)] * i / thres_int

        sample = sess.run(x_sample, feed_dict={xa_sample: xa_sample_ipt, _b_sample: _b_sample_ipt})

        save_dir = "./static/out/"
        #pylib.mkdir(save_dir)
        term = sample.squeeze(0)
        im.imwrite(term, '%s/%d.png' % (save_dir, 1))

        print("------------")






# input_data = "./test_images/000002.jpg"
#
# get_result(input_data, test_atts=['Male', 'Young'],test_ints=[0.4, -0.6])