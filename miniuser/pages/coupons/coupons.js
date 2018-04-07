// pages/coupons/coupons.js
const app = getApp()
var status = require('../../utils/error.js')

Page({
  data: {
    pointMall: []
  },

  onLoad: function() {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/point-mall',
      header: {'Authorization': 'Bearer ' + app.globalData.token},
      success: function(res) {
        if (res.statusCode === 200) {
          // console.log(res.data.userCoupons)
          that.setData({
            pointMall: res.data.pointMall
          })
          console.log(that.data)
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },

  getPromotion: function(e) {
    // console.log(e)
  }

})