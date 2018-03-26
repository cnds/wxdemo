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
    discountsObjectInput: {},
    discountObjectInput: {},
    discountsObject: {},
    discountBase: 0,
    discountMinus: 0,
    discountBaseInput: 0,
    discountMinusInput: 0,
    createDiscountObject: {},
    couponsArray: [],
    couponsObjectInput: {},
    couponObjectInput: {},
    createCouponObject: {},
    editReduction: false,
    editDiscount: false,
    createDiscount: true,
    editCoupon: false,
    createCoupon: false,
    editReductionHidden: false,
    editDiscountHidden: false,
    createDiscountHidden: false,
    editCouponHidden: false,
    createCouponHidden: false,
    delBtnWidth: 30,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    var that = this
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          windowWidth: res.windowWidth
        })
      }
    })
    this.getReductions()
    this.getDiscounts()
    this.getCoupons()
  },

  getReductions: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/reductions',
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
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/reductions',
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
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/discounts',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          var resultObject = util.resultArrayToObject(res.data.discounts)
          that.setData({
            discountsArray: res.data.discounts,
            discountsObject: resultObject
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
      discountsObjectInput: Object.assign(this.data.discountsObjectInput, { [currentId]: Object.assign(this.data.discountObjectInput, { base: parseInt(e.detail.value) }) })
    })
  },


  discountMinus: function (e) {
    var currentId = e.currentTarget.dataset.id
    this.setData({
      discountsObjectInput: Object.assign(this.data.discountsObjectInput, { [currentId]: Object.assign(this.data.discountObjectInput, { minus: parseInt(e.detail.value) }) })
    })
  },

  discountEdit: function (e) {
    this.setData({
      editDiscount: true,
      editDiscountHidden: true
    })
  },

  discountDone: function (e) {
    var that = this
    var discountsToInput = this.data.discountsObjectInput
    Object.keys(discountsToInput).forEach(function (key) {
      if (!discountsToInput[key].base) {
        Object.assign(discountsToInput[key], { base: that.data.discountsObject[key].base })
      }
      if (!discountsToInput[key].minus) {
        Object.assign(discountsToInput[key], { minus: that.data.discountsObject[key].minus })
      }
      wx.request({
        url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/discounts/' + key,
        method: 'PUT',
        header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
        data: discountsToInput[key],
        success: function (res) {
          if (res.statusCode === 200) {
            that.onLoad()
          } else if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      })
    })
    that.setData({
      editDiscountHidden: false,
      editDiscount: false
    })
  },

  createDiscount: function (e) {
    this.setData({
      createDiscountHidden: true,
    })
  },

  createDiscountDone: function (e) {
    var that = this
    var newDiscount = this.data.createDiscountObject
    if (Object.keys(newDiscount).length !== 0) {
      wx.request({
        url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/discounts',
        header: {'Authorization': 'Bearer ' + app.globalData.storeInfo.token},
        method: 'POST',
        data: newDiscount,
        success: function (res) {
          if (res.statusCode === 201) {
            that.setData({
              createDiscountObject: {}
            })
            that.onLoad()
          } else if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      })
    }
    this.setData({
      createDiscountHidden: false
    })
  },

  createDiscountBase: function (e) {
    this.setData({
      createDiscountObject: Object.assign(this.data.createDiscountObject, { base: parseInt(e.detail.value) })
    })
  },

  createDiscountMinus: function (e) {
    this.setData({
      createDiscountObject: Object.assign(this.data.createDiscountObject, { minus: parseInt(e.detail.value) })
    })
  },

  touchDiscountS: function (e) {
    if (e.touches.length === 1) {
      this.setData({
        startX: e.touches[0].clientX
      })
    }
  },

  touchDiscountM: function (e) {
    if (e.touches.length === 1) {
      var windowWidth = this.data.windowWidth
      var moveX = (e.touches[0].clientX / windowWidth) * 100
      var disX = (this.data.startX / windowWidth) * 100 - moveX
      var delBtnWidth = this.data.delBtnWidth
      var left = ""
      if (disX <= 0) {
        left = "margin-left:0rpx"
      } else {
        left = "margin-left:-" + disX + "vw"
        if (disX > delBtnWidth) {
          left = "margin-left:-" + delBtnWidth + "vw"
        }
      }
      var index = e.currentTarget.dataset.index
      if (index !== "" && index !== null) {
        var discountsArrayWithStyle = this.data.discountsArray
        Object.assign(discountsArrayWithStyle[index], { left: left })
        this.setData({
          discountsArray: discountsArrayWithStyle
        })
      }
    }
  },

  touchDiscountE: function (e) {
    if (e.changedTouches.length === 1) {
      var windowWidth = this.data.windowWidth
      var endX = e.changedTouches[0].clientX
      var disX = (this.data.startX - endX) / windowWidth * 100
      var delBtnWidth = this.data.delBtnWidth
      var left = disX > delBtnWidth / 2 ? "margin-left:-" + delBtnWidth + "vw" : "margin-left:0rpx"
      var index = e.currentTarget.dataset.index
      if (index !== "" && index !== null) {
        var discountsArrayWithStyle = this.data.discountsArray
        Object.assign(discountsArrayWithStyle[index], { left: left })
        this.setData({
          discountsArray: discountsArrayWithStyle
        })
      }
    }
  },

  deleteDiscount: function (e) {
    var that = this
    var currentId = e.currentTarget.dataset.id
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/discounts/' + currentId,
      header: {'Authorization': 'Bearer ' + app.globalData.storeInfo.token},
      method: 'DELETE',
      success: function (res) {
        if (res.statusCode === 200) {
          that.onLoad()
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  getCoupons: function (e) {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/coupons',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          var resultObject = util.resultArrayToObject(res.data.coupons)
          that.setData({
            couponsArray: res.data.coupons,
            couponsObject: resultObject
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
    var currentId = e.currentTarget.dataset.id
    this.setData({
      couponsObjectInput: Object.assign(this.data.couponsObjectInput, { [currentId]: Object.assign(this.data.couponObjectInput, { pay: parseInt(e.detail.value) }) })
    })
  },

  couponBase: function (e) {
    var currentId = e.currentTarget.dataset.id
    this.setData({
      couponsObjectInput: Object.assign(this.data.couponsObjectInput, { [currentId]: Object.assign(this.data.couponObjectInput, { base: parseInt(e.detail.value) }) })
    })
  },

  couponMinus: function (e) {
    var currentId = e.currentTarget.dataset.id
    this.setData({
      couponsObjectInput: Object.assign(this.data.couponsObjectInput, { [currentId]: Object.assign(this.data.couponObjectInput, { minus: parseInt(e.detail.value) }) })
    })
  },

  couponEdit: function (e) {
    this.setData({
      editCoupon: true,
      editCouponHidden: true
    })
  },

  couponDone: function (e) {
    var that = this
    var couponsToInput = this.data.couponsObjectInput
    Object.keys(couponsToInput).forEach(function (key) {
      if (!couponsToInput[key].pay) {
        Object.assign(couponsToInput[key], { pay: that.data.couponsObject[key].pay })
      }
      if (!couponsToInput[key].base) {
        Object.assign(couponsToInput[key], { base: that.data.couponsObject[key].base })
      }
      if (!couponsToInput[key].minus) {
        Object.assign(couponsToInput[key], { minus: that.data.couponsObject[key].minus })
      }
      wx.request({
        url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/coupons/' + key,
        method: 'PUT',
        header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
        data: couponsToInput[key],
        success: function (res) {
          if (res.statusCode === 200) {
            that.onLoad()
          } else if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      })
    })
    this.setData({
      editCoupon: false,
      editCouponHidden: false
    })
  },

  createCoupon: function (e) {
    this.setData({
      createCouponHidden: true
    })
  },

  createCouponDone: function (e) {
    var that = this
    var newCoupon = this.data.createCouponObject
    if (Object.keys(newCoupon).length !== 0) {
      wx.request({
        url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/coupons',
        header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
        method: 'POST',
        data: newCoupon,
        success: function (res) {
          if (res.statusCode === 201) {
            that.setData({
              createCouponObject: {}
            })
            that.onLoad()
          } else if (res.statusCode === 400) {
            status.status400(res.data.error)
          } else {
            status.status500()
          }
        }
      })
    }
    this.setData({
      createCouponHidden: false
    })
  },

  createCouponPay: function (e) {
    this.setData({
      createCouponObject: Object.assign(this.data.createCouponObject, { pay: parseInt(e.detail.value) })
    })
  },

  createCouponBase: function (e) {
    this.setData({
      createCouponObject: Object.assign(this.data.createCouponObject, { base: parseInt(e.detail.value) })
    })
  },

  createCouponMinus: function (e) {
    this.setData({
      createCouponObject: Object.assign(this.data.createCouponObject, { minus: parseInt(e.detail.value) })
    })
  },

  deleteCoupon: function (e) {
    var that = this
    var currentId = e.currentTarget.dataset.id
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/coupons/' + currentId,
      method: 'DELETE',
      header: { 'Authorization': 'Bearer ' + app.globalData.storeInfo.token },
      success: function (res) {
        if (res.statusCode === 200) {
          that.onLoad()
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  touchCouponS: function (e) {
    if (e.touches.length === 1) {
      this.setData({
        startX: e.touches[0].clientX
      })
    }
  },

  touchCouponM: function (e) {
    var windowWidth = this.data.windowWidth
    var moveX = (e.touches[0].clientX / windowWidth) * 100
    var disX = (this.data.startX / windowWidth) * 100 - moveX
    var delBtnWidth = this.data.delBtnWidth
    var left = ""
    if (disX <= 0) {
      left = "margin-left:0rpx"
    } else {
      left = "margin-left:-" + disX + "vw"
      if (disX > delBtnWidth) {
        left = "margin-left:-" + delBtnWidth + "vw"
      }
    }
    var index = e.currentTarget.dataset.index
    if (index !== "" && index !== null) {
      var couponsArrayWithStyle = this.data.couponsArray
      Object.assign(couponsArrayWithStyle[index], { left: left })
      this.setData({
        couponsArray: couponsArrayWithStyle
      })
    }
  },

  touchCouponE: function (e) {
    if (e.changedTouches.length === 1) {
      var windowWidth = this.data.windowWidth
      var endX = e.changedTouches[0].clientX
      var disX = (this.data.startX - endX) / windowWidth * 100
      var delBtnWidth = this.data.delBtnWidth
      var left = disX > delBtnWidth / 2 ? "margin-left:-" + delBtnWidth + "vw" : "margin-left:0rpx"
      var index = e.currentTarget.dataset.index
      if (index !== "" && index !== null) {
        var couponsArrayWithStyle = this.data.couponsArray
        Object.assign(couponsArrayWithStyle[index], { left: left })
        this.setData({
          couponsArray: couponsArrayWithStyle
        })
      }
    }
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
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/promotions',
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