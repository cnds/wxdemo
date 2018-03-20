// pages/coupons/coupons.js
const app = getApp()
var status = require('../../utils/error.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    coupons: []
  },

  onLoad: function() {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/users/' + app.globalData.userId + '/coupons',
      header: {'Authorization': 'Bearer ' + app.globalData.token},
      success: function(res) {
        if (res.statusCode === 200) {
          console.log(res.data.userCoupons)
          that.setData({
            coupons: res.data.userCoupons
          }) 
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  getPromotion: function(e) {
    console.log(e)
  }

})