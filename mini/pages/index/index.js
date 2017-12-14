// pages/demo/demo.js
const app = getApp()

Page({
  data: {
    transactions: null
  },
  transactionClick: function(event) {
    console.log(event)
  },
  onLoad: function(event) {
    var that = this
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.userInfo.id + '/transactions',
      header: 'Bearer ' + app.globalData.userInfo.token,
      success: function(res) {
        if (res.statusCode === 200) {
          that.setData({
            transactions: res.data.transactions
          })
          console.log(that.data)
        }
      }
    })
  }
})