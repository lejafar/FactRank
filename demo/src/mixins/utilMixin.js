import moment from "moment";

export default {
  methods: {
    formatDate: function(time_stamp, short = false) {
      // make sure this is recognized as UTC timestamp
      var published_at = moment(time_stamp);
      if (short) {
          return published_at.calendar(null, { lastWeek: `LL`, sameElse: `LL` });
      } else {
          return published_at.calendar(null, { sameElse: `LLL` });
      }
    }
  }
};
