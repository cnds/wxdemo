// pages/promotions/promotions.js
const app = getApp()
var status = require('../../utils/error.js')
var util = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    reductionPercent: null,
    reductionPercentInput: null,
    discountsArray: [],
    discountsArrayInput: [],
    discountsObject: {},
    discountObject: {},
    discountBase: 0,
    discountMinus: 0,
    discountBaseInput: 0,
    discountMinusInput: 0,
    couponPay: 0,
    couponBase: 0,
    couponMinus: 0,
    editReduction: false,
    editDiscount: false,
    createDiscount: true,
    editCoupon: false,
    createCoupon: false,
    editReductionHidden: false,
    editDiscountHidden: false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    this.getReductions()
    this.getDiscounts()
  },

  getReductions: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/reductions',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            reductionPercent: res.data.reductions[0].percent
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  reductionEdit: function () {
    this.setData({
      editReduction: true,
      editReductionHidden: true
    })
  },

  reductionPercentInput: function (e) {
    this.setData({
      reductionPercentInput: parseInt(e.detail.value)
    })
  },

  determineReduction: function () {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/reductions',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      data: {
        percent: this.data.reductionPercentInput
      },
      method: 'PUT',
      success: function (res) {
        if (res.statusCode === 200) {
          that.setData({
            reductionPercent: that.data.reductionPercentInput,
            editReduction: false,
            editReductionHidden: false,
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  reductionDone: function (e) {
    if (this.data.reductionPercentInput && this.data.reductionPercent !== this.data.reductionPercentInput) {
      this.determineReduction()
    } else {
      this.setData({
        editReduction: false,
        editReductionHidden: false,
      })
    }
  },

  getDiscounts: function (e) {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/discounts',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          // var resultObject = util.resultArrayToObject(res.data.discounts)
          that.setData({
            discountsArray: res.data.discounts,
            // discountsObject: resultObject
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
    var currentId = e.currentTarget.dataset.id
    this.setData({
      discountsObject: Object.assign(this.data.discountsObject, { [currentId]: Object.assign(this.data.discountObject, { base: parseInt(e.detail.value) }) })
    })
  },

  discountMinus: function (e) {
    var currentId = e.currentTarget.dataset.id
    this.setData({
      discountsObject: Object.assign(this.data.discountsObject, { [currentId]: Object.assign(this.data.discountObject, { minus: parseInt(e.detail.value) }) })
    })
  },

  discountEdit: function (e) {
    this.setData({
      editDiscount: true,
      editDiscountHidden: true
    })
  },

  editDiscountsArrayInput: function (discountsArrayInput, discountObject) {
    discountsArrayInput.push(discountObject)
  },

  discountDone: function (e) {
    console.log(this.data.discountsObject)
    var discountsToInput = this.data.discountsObject
    Object.keys(discountsToInput).forEach(function(key) {
      console.log(discountsToInput[key])
      wx.request({
        url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/discounts/' + key,
        method: 'PUT',
        header: {'Authorization': 'Bearer ' + app.globalData.storeInfo.token},
        data: discountsToInput[key],
        success: function(res) {
          console.log(res)
        }
      })
    }) 
    this.setData({
      editDiscountHidden: false
    })
  },

  getCoupons: function (e) {
    var that = this
    wx.request({
      url: 'localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/coupons',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
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

  couponBase: function (e) {
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
            editReduction: false,
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
      editReduction: false
    })
  },

})