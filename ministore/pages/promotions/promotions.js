// pages/promotions/promotions.js
const app = getApp()
var status = require('../../utils/error.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    reductionPercent: 0,
    couponPay: 0,
    couponBase: 0,
    couponMinus: 0,
    modifyReductions: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    this.getReductions()
    console.log(this.data)
  },

  getReductions: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/reductions',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          console.log(res)
          that.setData({
            reductionPercent: res.data.reductions.percent
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  modifyReductions: function () {
    this.setData({
      modifyReductions: true
    })
  },

  reductionPercent: function(e) {
    this.setData({
      reductionPercent: parseInt(e.detail.value)
    })
  },

  getDiscounts: function(e) {
    var that = this
    wx.request({
      url: 'localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + 'discounts',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function(res) {
        if (res.statusCode === 200) {
          that.setData({
            discountBase: res.data.discounts.base,
            discountMinus: res.data.discounts.minus
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
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

  getCoupons: function(e) {
    var that = this
    wx.request({
      url: 'localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + 'coupons',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function(res) {
        if (res.statusCode === 200) {
          that.setData({
            couponPay: res.data.coupons.pay,
            couponBase: res.data.coupons.base,
            couponMinus: res.data.coupons.minus
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
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
            modifyReductions: false,
          })
        } else if (res.statusCode === 400) {
            status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  cancel: function () {
    this.setData({
      modifyReductions: false
    })
  },

  // status400: function(e) {
  //   wx.showModal({
  //     title: '错误',
  //     content: e,
  //     showCancel: false
  //   })
  // },

  // status500: function(e) {
  //   wx.showModal({
  //     title: '错误',
  //     content: '服务器内部错误',
  //     showCancel: false
  //   })
  // }
})