export class DateUtils {

    static formatDate(date) {
        if (date) {

            const d = new Date(date);
            let month = '' + (d.getMonth() + 1);
            let day = '' + d.getDate();
            const year = d.getFullYear();

            if (month.length < 2) {
                month = '0' + month;
            }
            if (day.length < 2) {
                day = '0' + day;
            }
            return [year, month, day].join('-');
        } else {
            return null;
        }
    }

    static formatTime(time) {
        if (time && time.length === 5) {
            time = time + ':00';
        }
        return time;
    }

    // static formatHour
}
