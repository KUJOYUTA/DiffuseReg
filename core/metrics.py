import numpy as np
import torch


# import pystrum.pynd.ndutils as nd

def transform_grid(dDepth, dHeight, dWidth):
    batchSize = dDepth.shape[0]
    dpt = dDepth.shape[1]
    hgt = dDepth.shape[2]
    wdt = dDepth.shape[3]

    D_mesh = torch.linspace(0.0, dpt - 1.0, dpt).unsqueeze_(1).unsqueeze_(1).expand(dpt, hgt, wdt)
    h_t = torch.matmul(torch.linspace(0.0, hgt - 1.0, hgt).unsqueeze_(1), torch.ones((1, wdt)))
    H_mesh = h_t.unsqueeze_(0).expand(dpt, hgt, wdt)
    w_t = torch.matmul(torch.ones((hgt, 1)), torch.linspace(0.0, wdt - 1.0, wdt).unsqueeze_(1).transpose(1, 0))
    W_mesh = w_t.unsqueeze_(0).expand(dpt, hgt, wdt)

    D_mesh = D_mesh.unsqueeze_(0).expand(batchSize, dpt, hgt, wdt)
    H_mesh = H_mesh.unsqueeze_(0).expand(batchSize, dpt, hgt, wdt)
    W_mesh = W_mesh.unsqueeze_(0).expand(batchSize, dpt, hgt, wdt)
    D_upmesh = dDepth.float() + D_mesh
    H_upmesh = dHeight.float() + H_mesh
    W_upmesh = dWidth.float() + W_mesh
    return torch.stack([D_upmesh, H_upmesh, W_upmesh], dim=1)


def dice_ACDC(img_gt, img_pred, voxel_size=None):
    if img_gt.ndim != img_pred.ndim:
        raise ValueError("The arrays 'img_gt' and 'img_pred' should have the "
                         "same dimension, {} against {}".format(img_gt.ndim,
                                                                img_pred.ndim))
    # print(np.unique(img_gt))
    res = []
    # Loop on each classes of the input images
    for c in [3, 2, 4, 1, 5]:
        # Copy the gt image to not alterate the input
        gt_c_i = np.copy(img_gt)

        if c == 4:
            gt_c_i[gt_c_i == 2] = c
            gt_c_i[gt_c_i == 3] = c
        elif c == 5:
            gt_c_i[gt_c_i > 0] = c
        gt_c_i[gt_c_i != c] = 0

        # Copy the pred image to not alterate the input
        pred_c_i = np.copy(img_pred)

        if c == 4:
            pred_c_i[pred_c_i == 2] = c
            pred_c_i[pred_c_i == 3] = c
        elif c == 5:
            pred_c_i[pred_c_i > 0] = c
        pred_c_i[pred_c_i != c] = 0

        # Clip the value to compute the volumes
        gt_c_i = np.clip(gt_c_i, 0, 1)
        pred_c_i = np.clip(pred_c_i, 0, 1)
        # Compute the Dice
        top = 2 * np.sum(np.logical_and(pred_c_i, gt_c_i))
        bottom = np.sum(pred_c_i) + np.sum(gt_c_i)
        bottom = np.maximum(bottom, np.finfo(float).eps)  # add epsilon.
        dice = top / bottom

        if voxel_size != None:
            # Compute volume
            volpred = pred_c_i.sum() * np.prod(voxel_size) / 1000.
            volgt = gt_c_i.sum() * np.prod(voxel_size) / 1000.
        else:
            volpred, volgt = 0, 0

        res += [dice, volpred, volpred - volgt]

    return res


def dice_BraTS(img_gt, img_pred, voxel_size=None):
    if img_gt.ndim != img_pred.ndim:
        raise ValueError("The arrays 'img_gt' and 'img_pred' should have the "
                         "same dimension, {} against {}".format(img_gt.ndim,
                                                                img_pred.ndim))
    # print(np.unique(img_gt))
    res = []
    # Loop on each classes of the input images
    for c in [3, 2, 1]:
        # Copy the gt image to not alterate the input
        gt_c_i = np.copy(img_gt)

        if c == 4:
            gt_c_i[gt_c_i == 2] = c
            gt_c_i[gt_c_i == 3] = c
        elif c == 5:
            gt_c_i[gt_c_i > 0] = c
        gt_c_i[gt_c_i != c] = 0

        # Copy the pred image to not alterate the input
        pred_c_i = np.copy(img_pred)

        if c == 4:
            pred_c_i[pred_c_i == 2] = c
            pred_c_i[pred_c_i == 3] = c
        elif c == 5:
            pred_c_i[pred_c_i > 0] = c
        pred_c_i[pred_c_i != c] = 0

        # Clip the value to compute the volumes
        gt_c_i = np.clip(gt_c_i, 0, 1)
        pred_c_i = np.clip(pred_c_i, 0, 1)
        # Compute the Dice
        top = 2 * np.sum(np.logical_and(pred_c_i, gt_c_i))
        bottom = np.sum(pred_c_i) + np.sum(gt_c_i)
        bottom = np.maximum(bottom, np.finfo(float).eps)  # add epsilon.
        dice = top / bottom

        if voxel_size != None:
            # Compute volume
            volpred = pred_c_i.sum() * np.prod(voxel_size) / 1000.
            volgt = gt_c_i.sum() * np.prod(voxel_size) / 1000.
        else:
            volpred, volgt = 0, 0

        res += [dice, volpred, volpred - volgt]

    return res


def jacc_ACDC(img_gt, img_pred, voxel_size=None):
    if img_gt.ndim != img_pred.ndim:
        raise ValueError("The arrays 'img_gt' and 'img_pred' should have the "
                         "same dimension, {} against {}".format(img_gt.ndim,
                                                                img_pred.ndim))
    # print(np.unique(img_gt))
    res = []
    # Loop on each classes of the input images
    for c in [3, 2, 4, 1, 5]:
        # Copy the gt image to not alterate the input
        gt_c_i = np.copy(img_gt)

        if c == 4:
            gt_c_i[gt_c_i == 2] = c
            gt_c_i[gt_c_i == 3] = c
        elif c == 5:
            gt_c_i[gt_c_i > 0] = c
        gt_c_i[gt_c_i != c] = 0

        # Copy the pred image to not alterate the input
        pred_c_i = np.copy(img_pred)

        if c == 4:
            pred_c_i[pred_c_i == 2] = c
            pred_c_i[pred_c_i == 3] = c
        elif c == 5:
            pred_c_i[pred_c_i > 0] = c
        pred_c_i[pred_c_i != c] = 0

        # Clip the value to compute the volumes
        gt_c_i = np.clip(gt_c_i, 0, 1)
        pred_c_i = np.clip(pred_c_i, 0, 1)
        # Compute the Jacc
        top = np.sum(np.logical_and(pred_c_i, gt_c_i))
        bottom = np.sum(np.logical_or(pred_c_i, gt_c_i))
        bottom = np.maximum(bottom, np.finfo(float).eps)  # add epsilon.
        jacc = top / bottom

        if voxel_size != None:
            # Compute volume
            volpred = pred_c_i.sum() * np.prod(voxel_size) / 1000.
            volgt = gt_c_i.sum() * np.prod(voxel_size) / 1000.
        else:
            volpred, volgt = 0, 0

        res += [jacc, volpred, volpred - volgt]

    return res


def mask_metrics(seg1, seg2):
    ''' Given two segmentation seg1, seg2, 0 for background 255 for foreground.
    Calculate the Dice score
    $ 2 * | seg1 \cap seg2 | / (|seg1| + |seg2|) $
    and the Jacc score
    $ | seg1 \cap seg2 | / (|seg1 \cup seg2|) $
    '''
    sizes = torch.prod(torch.tensor(seg1.shape[1:]))
    seg1 = seg1.reshape(-1, sizes)
    seg2 = seg2.reshape(-1, sizes)
    dice_score = 2.0 * torch.sum(seg1 * seg2, dim=-1) / (
            torch.sum(seg1, dim=-1) + torch.sum(seg2, dim=-1))
    union = torch.sum(torch.max(seg1, seg2), dim=-1)
    # return (dice_score,
    #         torch.sum(torch.min(seg1, seg2), dim=-1) / torch.max(union, torch.tensor(0.01))
    #         )
    return dice_score


def get_jacobian_determinant(flow):
    e1 = torch.reshape(torch.Tensor([1, 0, 0]), (1, 3, 1, 1, 1)).type(torch.float32).cuda()
    e2 = torch.reshape(torch.Tensor([0, 1, 0]), (1, 3, 1, 1, 1)).type(torch.float32).cuda()
    e3 = torch.reshape(torch.Tensor([0, 0, 1]), (1, 3, 1, 1, 1)).type(torch.float32).cuda()

    stacks = torch.stack([
        flow[..., 1:, :-1, :-1] - flow[..., :-1, :-1, :-1] + e1,
        flow[..., :-1, 1:, :-1] - flow[..., :-1, :-1, :-1] + e2,
        flow[..., :-1, :-1, 1:] - flow[..., :-1, :-1, :-1] + e3
    ], dim=2)
    stacks = torch.permute(stacks, [0, 3, 4, 5, 1, 2])
    determinant = torch.linalg.det(stacks)
    return determinant


def jacobian_det_var(flow):
    determinant = get_jacobian_determinant(flow)
    variance = torch.var(determinant, dim=[1, 2, 3])
    return torch.sqrt(variance)


def neg_jacobian_det(flow):
    determinant = get_jacobian_determinant(flow)
    neg = (determinant <= 0).sum(dim=[1, 2, 3]) / torch.prod(torch.tensor(determinant.size()[1:]))
    return neg * 100
