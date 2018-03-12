const errMsg = {
  'INVALID_BODY_CONTENT': '输入格式错误',
  'INVALID_QUERY_PARAMS': '查询参数错误',
  'CONFLICT_USER_EXIST': '重复用户',
  'USER_NOT_FOUND': '用户不存在',
  'NOT_FOUND': '未找到',
  'PASSWORD_VERIFICATION_FAILED': '密码错误',
  'SMS_CODE_VERIFICATION_FAILED': '短信验证码错误',
  'ATTEMPT_TOO_MANY_TIMES': '尝试次数过多',
  'AUTHENTICATION_INFO_REQUIRED': '缺少鉴权信息',
  'AUTHENTICATION_INFO_ILLEGAL': '非法的鉴权信息',
  'PERMISSION_DENIED': '没有权限',
  'OPERATION_FAILED': '操作失败',
  'INVALID_WX_CODE': '错误的二维码',
  'QR_CODE_NOT_EXIST': '二维码不存在',
  'STORE_NOT_EXIST': '店铺不存在',
  'QR_CODE_ALREADY_BEEN_BOUND': '二维码已被绑定',
  'CONFLICT_COUPON': '重复的优惠券',
  'COUPON_NOT_EXIST': '优惠券不存在',
  'COUPON_HAS_BEEN_REMOVED': '优惠券已被删除',
  'PROMOTION_NOT_EXIST': '优惠不存在',
  'DB_BULK_UPDATE_ERROR': '批量操作失败',
  'CONFLICT_DISCOUNT': '重复的满减',
  'DISCOUNT_NOT_EXIST': '满减不存在',
  'DISCOUNT_HAS_BEEN_REMOVED': '满减信息已被删除',
  'REDUCTION_HAS_BEEN_REMOVED': '折扣已被删除',
  'REDUCTION_NOT_EXIST': '折扣不存在',
  'USER_COUPON_NOT_EXIST': '用户优惠券不存在',
  'STORE_HAVE_NOT_BOUND_QR_CODE': '用户未绑定小程序二维码',
}

function status400(e) {
  var content = '未知错误'
  if (e in errMsg) {
    content = errMsg[e]
  }
  wx.showModal({
    title: '错误',
    content: content,
    showCancel: false
  })
}

function status500() {
  wx.showModal({
    title: '错误',
    content: '服务器内部错误',
    showCancel: false
  })
}

module.exports.status400 = status400
module.exports.status500 = status500