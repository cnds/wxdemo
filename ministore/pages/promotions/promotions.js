// pages/promotions/promotions.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    discountBase: 0,
    discountMinus: 0,
    couponPay: 0,
    couponBase: 0,
    couponMinus: 0,
    modifyPromotions: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    this.getPromotions()
  },

  getPromotions: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/promotions',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            discountBase: res.data.discount.base,
            discountMinus: res.data.discount.minus,
            couponPay: res.data.coupon.pay,
            couponBase: res.data.coupon.base,
            couponzMinus: res.data.coupon.minus
          })
        }
      }
    })
  },

  modifyPromotions: function () {
    this.setData({
      modifyPromotions: true
    })
  },

  discountBase: function (e) {
    this.setData({
      discountBase: parseInt(e.detail.value)
    })
  },

  discountMinus: function (e) {
    this.setData({
      discountMinus: parseInt(e.detail.value)
    })
  },

  couponPay: function (e) {
    this.setData({
      couponPay: parseInt(e.detail.value)
    })
  },

  couponBase: function(e) {
    this.setData({
      couponBase: parseInt(e.detail.value)
    })
  },

  couponMinus: function (e) {
    this.setData({
      couponMinus: parseInt(e.detail.value)
    })
  },

  determine: function () {
    var that = this
    if (this.data.discountMinus > this.data.discountBase || this.data.couponMinus > this.data.couponBase) {
      wx.showModal({
        title: '提示',
        content: '折扣金额不能大于基础金额',
        showCancel: false,
      })
    }
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/promotions',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      data: {
        discount: { base: this.data.discountBase, minus: this.data.discountMinus },
        coupon: { pay: this.data.couponPay, base: this.data.couponBase, minus: this.data.couponMinus }
      },
      method: 'PUT',
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            modifyPromotions: false,
          })
        } else if (res.statusCode === 400) {
          wx.showModal({
            title: '错误',
            content: res.data.error,
            showCancel: false
          })
        } else {
          wx.showModal({
            title: '错误',
            content: '服务器内部错误',
            showCancel: false
          })
        }
      }
    })
  },

  cancel: function () {
    this.setData({
      modifyPromotions: false
    })
  }
})