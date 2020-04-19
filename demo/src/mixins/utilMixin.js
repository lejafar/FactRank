import moment from "moment";

export default {
  methods: {
    formatDate: function(time_stamp, short = false) {
      // make sure this is recognized as UTC timestamp
      let published_at = moment(time_stamp);
      if (published_at.tz("GMT").hour() == 0 && published_at.minutes() == 0){
          let datestring = published_at.calendar(null, { sameElse: `LLL` })
          if (datestring.includes('om')){
              return datestring.slice(0, -8);
          }
          return datestring.slice(0, -5);
      }
      if (short) {
          return published_at.calendar(null, { lastWeek: `LL`, sameElse: `LL` }).slice(0, -5);
      } else {
          return published_at.calendar(null, { sameElse: `LLL` });
      }
    }
  }
};
