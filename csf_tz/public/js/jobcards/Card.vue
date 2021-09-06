<template>
  <div justify="center" v-if="Dialog">
    <v-dialog v-model="Dialog" max-width="900">
      <v-card class="px-3">
        <v-card-title class="mt-2">
          <span class="headline indigo--text">{{
            cardData.operation.name
          }}</span>
          <v-spacer></v-spacer>
          <div
            class="stopwatch"
            style="
              font-weight: bold;
              margin: 0px 13px 0px 2px;
              color: #545454;
              font-size: 18px;
              display: inline-block;
              vertical-align: text-bottom;
            "
          >
            <span class="hours">{{ timer.hours }}</span>
            <span class="colon">:</span>
            <span class="minutes">{{ timer.minutes }}</span>
            <span class="colon">:</span>
            <span class="seconds">{{ timer.seconds }}</span>
          </div>
          <v-spacer></v-spacer>
          <span class="overline">{{ cardData.name }}</span>
        </v-card-title>
        <v-row class="mx-3">
          <v-col lg="5" md="5" cols="12">
            <v-list-item-subtitle class="subtitle-1 mb-1">
              Status: {{ cardData.status }}
            </v-list-item-subtitle>
          </v-col>
          <v-col lg="4" md="4" cols="12">
            <v-textarea
              label="Operation Description"
              auto-grow
              outlined
              rows="3"
              row-height="25"
              readonly
              v-model="cardData.operation.description"
              hide-details
            >
            </v-textarea>
          </v-col>
          <v-col lg="3" md="3" cols="12">
            <v-list-item-subtitle class="subtitle-1 mb-1">
              Production Item: {{ cardData.production_item }}
            </v-list-item-subtitle>
            <v-divider></v-divider>
            <v-autocomplete
              dense
              auto-select-first
              outlined
              color="indigo"
              label="Team Leader"
              v-model="cardData.employee"
              :items="employees"
              item-text="name"
              background-color="white"
              no-data-text="Employee not found"
              hide-details
              :readonly="cardData.employee ? true : false"
              :filter="customFilter"
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="indigo--text subtitle-1"
                      v-html="data.item.name"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-html="`${data.item.employee_name}`"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
        <v-row class="mx-3">
          <v-col lg="9" md="9" cols="12">
            <v-autocomplete
              dense
              auto-select-first
              outlined
              color="indigo"
              label="Station Members"
              v-model="members"
              :items="employees"
              item-text="name"
              background-color="white"
              no-data-text="Employee not found"
              hide-details
              :filter="customFilter"
              multiple
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="indigo--text subtitle-1"
                      v-html="data.item.name"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-html="`${data.item.employee_name}`"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col lg="9" md="9" cols="12">
            <v-textarea
              class="my-2"
              label="Remarks"
              auto-grow
              outlined
              rows="2"
              row-height="25"
              v-model="cardData.remarks"
              hide-details
            >
            </v-textarea>
          </v-col>
          <v-col lg="3" md="3" cols="12">
            <v-list-item-subtitle class="subtitle-1 mb-1">
              Qty To Manufacture: {{ cardData.for_quantity }}
            </v-list-item-subtitle>
            <v-list-item-subtitle class="subtitle-1 mb-1">
              Qty Completed: {{ cardData.total_completed_qty }}
            </v-list-item-subtitle>
          </v-col>
        </v-row>
        <v-card-actions class="mx-3">
          <v-btn
            v-if="
              !cardData.job_started &&
              cardData.total_completed_qty != cardData.for_quantity
            "
            @click="start_por"
            color="success"
            dark
            >Start</v-btn
          >
          <v-btn
            v-if="
              cardData.status == 'On Hold' &&
              cardData.total_completed_qty != cardData.for_quantity
            "
            @click="resume_por"
            color="warning"
            dark
            >Resume</v-btn
          >
          <v-btn
            v-if="
              cardData.status == 'Work In Progress' &&
              cardData.total_completed_qty != cardData.for_quantity
            "
            @click="pause_por"
            color="warning"
            dark
            >Stop</v-btn
          >
          <v-spacer></v-spacer>
          <v-text-field
            v-if="
              cardData.status == 'Work In Progress' &&
              cardData.total_completed_qty != cardData.for_quantity
            "
            outlined
            color="indigo"
            label="Completed Qty"
            background-color="white"
            hide-details
            v-model="completed_qty"
            type="number"
            dense
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            dark
            @click="submit_dialog"
            v-if="
              cardData.total_completed_qty == cardData.for_quantity &&
              cardData.status != 'Completed'
            "
            >Submit</v-btn
          >
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { evntBus } from './bus';
export default {
  data: () => ({
    Dialog: false,
    cardData: '',
    employees: '',
    members: [],
    completed_qty: 1,
    timer: {
      hours: '00',
      minutes: '00',
      seconds: '00',
      interval: '',
    },
  }),
  watch: {
    Dialog(value) {
      if (value) {
        this.get_employees();
      } else {
        clearInterval(this.timer.interval);
      }
    },
  },
  methods: {
    close_dialog() {
      this.Dialog = false;
    },
    start_job() {
      let row = frappe.model.add_child(
        this.cardData,
        'Job Card Time Log',
        'time_logs'
      );
      row.from_time = frappe.datetime.now_datetime();
      row.name = '';
      row.completed_qty = 1;
      this.cardData.job_started = 1;
      this.cardData.started_time = row.from_time;
      this.cardData.status = 'Work In Progress';
      if (!frappe.flags.resume_job) {
        this.cardData.current_time = 0;
      }
      this.set_timer();
      this.save();
    },
    start_por() {
      if (!this.cardData.employee) {
        evntBus.$emit('show_messag', 'Please set Employee');
      } else {
        this.start_job();
      }
    },
    resume_por() {
      frappe.flags.resume_job = 1;
      this.start_job();
    },
    pause_por() {
      if (
        this.cardData.for_quantity <
        this.cardData.total_completed_qty + flt(this.completed_qty)
      ) {
        evntBus.$emit(
          'show_messag',
          'The completed quantity cannot be greater than the required quantity'
        );
        return;
      }
      frappe.flags.pause_job = 1;
      this.cardData.status = 'On Hold';
      clearInterval(this.timer.interval);
      this.complete_job();
    },
    get_employees() {
      const vm = this;
      let employees;
      frappe.call({
        method: 'csf_tz.csf_tz.page.jobcards.jobcards.get_employees',
        args: { company: this.cardData.company },
        async: false,
        callback: function (r) {
          if (r.message) {
            employees = r.message;
          }
        },
      });
      this.employees = employees;
    },
    customFilter(item, queryText, itemText) {
      const searchText = queryText.toLowerCase();
      const textOne = item.name.toLowerCase();
      const textTwo = item.employee_name.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 || textTwo.indexOf(searchText) > -1
      );
    },
    set_timer() {
      if (this.cardData.status == 'Completed') {
        return;
      }
      const vm = this;
      let currentIncrement = this.cardData.current_time || 0;
      if (this.cardData.started_time || this.cardData.current_time) {
        if (this.cardData.status == 'On Hold') {
          updateStopwatch(currentIncrement);
          clearInterval(this.timer.interval);
        } else {
          currentIncrement += moment(frappe.datetime.now_datetime()).diff(
            moment(this.cardData.started_time),
            'seconds'
          );
          initialiseTimer();
        }

        function initialiseTimer() {
          vm.timer.interval = setInterval(() => {
            var current = setCurrentIncrement();
            updateStopwatch(current);
          }, 1000);
        }

        function updateStopwatch(increment) {
          const hours = Math.floor(increment / 3600);
          const minutes = Math.floor((increment - hours * 3600) / 60);
          const seconds = increment - hours * 3600 - minutes * 60;

          vm.timer.hours =
            hours < 10 ? '0' + hours.toString() : hours.toString();
          vm.timer.minutes =
            minutes < 10 ? '0' + minutes.toString() : minutes.toString();
          vm.timer.seconds =
            seconds < 10 ? '0' + seconds.toString() : seconds.toString();
        }

        function setCurrentIncrement() {
          currentIncrement += 1;
          return currentIncrement;
        }
      }
    },
    complete_job(completed_time) {
      const idx = this.cardData.time_logs.length - 1;
      this.cardData.time_logs[idx].completed_qty = flt(this.completed_qty);
      this.completed_qty = 1;
      this.cardData.time_logs.forEach((d) => {
        if (d.from_time && !d.to_time) {
          d.to_time = completed_time || frappe.datetime.now_datetime();

          if (frappe.flags.pause_job) {
            let currentIncrement =
              moment(d.to_time).diff(moment(d.from_time), 'seconds') || 0;
            this.cardData.current_time =
              currentIncrement + (this.cardData.current_time || 0);
          } else {
            this.cardData.started_time = '';
            this.cardData.job_started = 0;
            this.cardData.current_time = 0;
          }
          this.save();
        }
      });
    },
    submit_dialog() {
      this.cardData.status = 'Completed';
      this.save('Submit');
      this.close_dialog();
    },
    save(action = 'Save') {
      const vm = this;
      const doc = { ...this.cardData };
      doc.members = [];
      this.members.forEach((element) => {
        let employee_name =
          this.employees.find((emp) => emp.name == element).employee_name || '';
        doc.members.push({ employee: element, employee_name: employee_name });
      });

      delete doc['operation'];
      frappe.call({
        method: 'csf_tz.csf_tz.page.jobcards.jobcards.save_doc',
        args: {
          doc: doc,
          action: action,
        },
        async: false,
        callback: function (r) {
          if (r.message) {
            r.message.operation = vm.cardData.operation;
            vm.members = [];
            r.message.members.forEach((element) => {
              vm.members.push(element.employee);
            });
            Object.assign(vm.cardData, r.message);
          }
        },
      });
    },
  },
  created: function () {
    evntBus.$on('open_card', (job_card) => {
      const vm = this;
      this.Dialog = true;
      this.cardData = job_card;
      this.members = [];
      frappe.call({
        method: 'frappe.client.get',
        args: {
          doctype: 'Job Card',
          name: job_card.name,
        },
        callback(r) {
          if (r.message) {
            vm.cardData = r.message;
            r.message.members.forEach((element) => {
              vm.members.push(element.employee);
            });
            vm.timer = {
              hours: '00',
              minutes: '00',
              seconds: '00',
            };
            vm.set_timer();
          }
        },
      });
    });
  },
};
</script>

<style>
</style>