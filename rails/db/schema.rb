# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20150211131503) do

  create_table "internships", force: :cascade do |t|
    t.string  "address"
    t.string  "company"
    t.string  "branch"
    t.string  "branch_abbreviation"
    t.text    "description"
    t.string  "student"
    t.string  "level"
    t.string  "level_abbreviation"
    t.string  "subject"
    t.string  "semester"
    t.integer "year"
    t.string  "teacher"
    t.string  "city"
    t.string  "country"
    t.string  "filiere"
    t.string  "filiere_abbreviation"
    t.float   "latitude"
    t.float   "longitude"
    t.boolean "done"
    t.boolean "confidential"
  end

end
