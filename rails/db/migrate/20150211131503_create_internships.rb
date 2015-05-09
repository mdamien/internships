class CreateInternships < ActiveRecord::Migration
  def change
    create_table :internships do |t|
      t.string  :address
      t.string  :company
      t.string  :branch
      t.text    :description
      t.string  :student
      t.string  :level
      t.string  :subject
      t.string  :semester
      t.integer :year
      t.string  :teacher
      t.string  :city
      t.string  :country
      t.string  :filiere
      t.float   :latitude
      t.float   :longitude
      t.boolean :done
      t.boolean :confidential
    end
  end
end