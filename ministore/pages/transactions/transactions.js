// pages/transactions/transactions.js
const app = getApp()

Page({
  data: {
    orders: null
  },
  transactionClick: function(event) {
    console.log(event)
  },
  onLoad: function(event) {
    var that = this
    console.log(app.globalData.storeInfo.token)
    wx.request({
      url: 'http://localhost:10000/gateway/stores/' + app.globalData.storeInfo.id + '/orders',
      header: {'Authorization': 'Bearer ' + app.globalData.storeInfo.token},
      success: function(res) {
        if (res.statusCode === 200) {
          that.setData({
            orders: res.data.orders
          })
          console.log(that.data)
        }
      }
    })
  }
})