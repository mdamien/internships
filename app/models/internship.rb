class Internship < ActiveRecord::Base
  enum semester: [ :A, :P ]
end