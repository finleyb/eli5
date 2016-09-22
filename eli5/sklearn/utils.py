# -*- coding: utf-8 -*-
import numpy as np


def is_multiclass_classifier(clf):
    """
    Return True if a classifier is multiclass or False if it is binary.
    """
    return clf.coef_.shape[0] > 1


def is_multitarget_regressor(clf):
    """
    Return True if a regressor is multitarget
    or False if it predicts a single target.
    """
    return len(clf.coef_.shape) > 1 and clf.coef_.shape[0] > 1


def is_probabilistic_classifier(clf):
    """ Return True if a classifier can return probabilities """
    return hasattr(clf, 'predict_proba')


def has_intercept(clf):
    """ Return True if classifier has intercept fit. """
    return getattr(clf, 'fit_intercept', False)


def get_feature_names(clf, vec=None, bias_name='<BIAS>', feature_names=None):
    """
    Return a vector of feature names, including bias feature.
    If vec is None or doesn't have get_feature_names() method,
    features are named x1, x2, etc.
    """
    if feature_names is None:
        if vec and hasattr(vec, 'get_feature_names'):
            feature_names = list(vec.get_feature_names())
        else:
            num_features = clf.coef_.shape[-1]
            feature_names = ["x%d" % i for i in range(num_features)]
    else:
        num_features = clf.coef_.shape[-1]
        if len(feature_names) != num_features:
            raise ValueError("feature_names has a wrong length: "
                             "expected=%d, got=%d" % (num_features,
                                                      len(feature_names)))
    if bias_name is not None and has_intercept(clf):
        feature_names += [bias_name]
    return np.array(feature_names)


def get_target_names(clf):
    """
    Return a vector of target names: y if the is only one target,
    and y0, ... if there are multiple targets.
    """
    if len(clf.coef_.shape) == 1:
        target_names = ['y']
    else:
        num_targets, _ = clf.coef_.shape
        target_names = ['y%d' % i for i in range(num_targets)]
    return np.array(target_names)


def get_coef(clf, label_id):
    """
    Return a vector of coefficients for a given label,
    including bias feature.
    """
    if len(clf.coef_.shape) == 2:
        # Most classifiers (even in binary case) and regressors
        coef = clf.coef_[label_id]
    elif len(clf.coef_.shape) == 1:
        # SGDRegressor stores coefficients in a 1D array
        if label_id != 0:
            raise ValueError(
                'Unexpected label_id %s for 1D coefficient' % label_id)
        coef = clf.coef_
    else:
        raise ValueError('Unexpected clf.coef_ shape: %s' % clf.coef_.shape)
    if not has_intercept(clf):
        return coef
    if label_id == 0 and not isinstance(clf.intercept_, np.ndarray):
        bias = clf.intercept_
    else:
        bias = clf.intercept_[label_id]
    return np.hstack([coef, bias])


def rename_label(label_id, label, target_names):
    """ Rename label according to target_names """
    if target_names is None:
        return label
    if isinstance(target_names, dict):
        return target_names[label]
    return target_names[label_id]