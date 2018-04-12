// pages/payment/payment.js
const app = getApp()
var status = require('../../utils/error.js')
var QRCode = require('../../utils/qrcode.js')
var config = require('../../utils/config.js')

Page({
  data: {
    hasPaymentDetail: false,
    showStorePaymentCode: false,
    showPointPasswordInput: false
  },

  onLoad: function (options) {
    app.globalData.scene = null
    if (app.globalData.userId && app.globalData.token) {
      this.getStoreInfo()
    } else {
      this.registerUser()
    }
  },

  login: function (openId) {
    var that = this
    wx.request({
      url: config.config.authorization + '/user-sessions',
      data: { openId: openId },
      method: 'POST',
      success: function (res) {
        if (res.statusCode === 201) {
          app.globalData.token = res.data.token
          app.globalData.userId = res.data.id
          that.getStoreInfo()
          wx.showToast({
            title: '登录成功',
          })
        } else {
          wx.showModal({
            title: '错误',
            content: '登录失败',
            showCancel: false
          })
        }
      }
    })
  },

  registerUser: function () {
    var that = this
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        var code = res.code
        // console.log(res)
        wx.getSetting({
          success: res => {
            // console.log(res)
            wx.getUserInfo({
              success: res => {
                // 可以将 res 发送给后台解码出 unionId
                app.globalData.userInfo = res.userInfo
                // console.log(res)
                var iv = res.iv
                var encryptedData = res.encryptedData

                // 查看用户注册状态，如果未注册，创建用户后登录，如已注册则直接登录
                wx.request({
                  url: config.config.authorization + '/users/register-status',
                  data: { code: code },
                  method: 'POST',
                  success: function (res) {
                    if (res.statusCode === 201) {
                      that.login(res.data.openId)
                    } else if (res.statusCode === 400) {
                      wx.login({
                        success: res => {
                          var code = res.code
                          wx.request({
                            url: config.config.authorization + '/users',
                            data: {
                              code: code,
                              iv: iv,
                              encryptedData: encryptedData
                            },
                            method: 'POST',
                            success: function (res) {
                              wx.hideLoading();
                              that.login(res.data.id);
                            }
                          })
                        }
                      })
                    }
                  }
                })
                // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                // 所以此处加入 callback 以防止这种情况
                if (this.userInfoReadyCallback) {
                  this.userInfoReadyCallback(res)
                }
              }
            })
          }
        })
      }
    })
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
      amount: parseFloat(e.detail.value)
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
          that.setData({
            reductionPercent: null,
            discountBase: null,
            discountMinus: null,
            couponMinus: null,
            couponPoint: null,
            actualAmount: null,
            hasPaymentDetail: false
          })
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
            actualAmount: parseFloat((res.data.actualAmount).toFixed(1)),
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
      data: { storeId: this.data.storeId, point: parseInt(this.data.actualAmount) },
      success: function (res) {
        if (res.statusCode === 201) {
          wx.showToast({
            title: '领取优惠成功',
          })
          that.setData({
            showPointPasswordInput: false
          })
          wx.redirectTo({
            url: '../index/index',
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