// pages/promotions/promotions.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    promotions: []
  },

  onLoad: function() {
    wx.request({
      url: 'http://localhost:10000/gateway/users/' + app.globalData.userId + '/promotions',
      header: {'Authorization': 'Bearer ' + app.globalData.token},
      success: function(res) {
        console.log(res)
        if (res.statusCode === 200) {
          this.setData({
            promotions: res.data.promotions
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

  getPromotion: function(e) {
    console.log(e)
  }

})