// pages/payment/payment.js
const app = getApp()
var status = require('../../utils/error.js')
var QRCode = require('../../utils/qrcode.js')

Page({
  data: {
    hasPaymentDetail: false,
    showStorePaymentCode: false,
    showPointPasswordInput: false
  },

  onLoad: function (options) {
    this.getStoreInfo()
  },

  getStoreInfo: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/store-info/' + app.globalData.code,
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            storeId: res.data.id,
            storeName: res.data.storeName,
            address: res.data.address
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  Amount: function (e) {
    this.setData({
      amount: parseInt(e.detail.value)
    })
  },

  getPaymentDetail: function (e) {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/payment-detail',
      method: 'POST',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      data: { storeId: that.data.storeId, amount: that.data.amount },
      success: function (res) {
        console.log(res.data)
        if (res.statusCode === 201) {
          if (res.data.reduction) {
            that.setData({
              reductionPercent: res.data.reduction.percent,
            })
          }
          if (res.data.discount) {
            that.setData({
              discountBase: res.data.discount.base,
              discountMinus: res.data.discount.minus,
            })
          }
          if (res.data.coupon) {
            that.setData({
              couponMinus: res.data.coupon.minus,
              couponPoint: res.data.coupon.point
            })
          }
          that.setData({
            actualAmount: parseInt(res.data.actualAmount),
            hasPaymentDetail: true
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  getPoints: function () {
    this.setData({
      showPointPasswordInput: true
    })
  },

  pointPasswordInput: function (e) {
    this.setData({
      pointPasswordInput: e.detail.value
    })

  },

  pointPasswordDetermine: function () {
    this.checkPointPassword()
  },

  pointPasswordCancel: function () {
    this.setData({
      showPointPasswordInput: false
    })
  },

  checkPointPassword: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/password-checker',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      method: 'POST',
      data: { storeId: this.data.storeId, pointPassword: this.data.pointPasswordInput },
      success: function (res) {
        if (res.statusCode === 201) {
          that.createOrder()
          that.setData({
            pointPasswordInput: null
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  createOrder: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/orders',
      method: 'POST',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      data: { storeId: this.data.storeId, amount: this.data.actualAmount },
      success: function (res) {
        if (res.statusCode === 201) {
          that.increasePoints()
          if (that.data.couponPoint) {
            that.decreasePoints()
          }
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  increasePoints: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/points/increase',
      method: 'POST',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      data: { storeId: this.data.storeId, point: this.data.actualAmount },
      success: function (res) {
        if (res.statusCode === 201) {
          wx.showToast({
            title: '领取优惠成功',
          })
          that.setData({
            showPointPasswordInput: false
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  decreasePoints: function () {
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/points/decrease',
      method: 'POST',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      data: { storeId: this.data.storeId, point: this.data.couponPoint },
      success: function (res) {
        if (res.statusCode !== 201) {
          if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      }
    })
  }
})