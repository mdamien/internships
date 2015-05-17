require 'csv'

namespace :app do
  desc "Import internships from csv file"
  
  task :import, [:file] => [:environment] do |t,args|
    file = args[:file]

    puts "deleting previous internships"
    Internship.delete_all

    puts "loading csv"

    ActiveRecord::Base.transaction do
      CSV.foreach(file,
        :headers => true) do |row|

          Internship.create({
            address: row['addresse'],
            branch: row['branche'],
            branch_abbreviation: row['branche_abbrev'],
            city: row['city'],
            company: row['company'],
            confidential: row['confidentiel'] == "x" ? true : false,
            country: row['country'],
            description: row['description'],
            done: row['done'] == "x" ? true : false,
            student: row['etudiant'],
            filiere: row['filiere'],
            filiere_abbreviation: row['filiere_abbrev'],
            latitude: row['lat'],
            longitude: row['lng'],
            level: row['niveau'],
            level_abbreviation: row['niveau_abbrev'],
            id: row['num'],
            year: row['semestre_annee'],
            semester: row['semestre'],
            subject: row['sujet'],
            teacher: row['teacher']
          })

          if $. % 100 == 0 then puts $. end
      end
    end
  end

  task :import_fake_data, [:file] => [:environment] do |t,args|
    file = args[:file]

    Internship.delete_all

    #num,addresse,branche_abbrev,filiere,company,description,etudiant,niveau,semestre,semestre_annee,sujet,tuteur,done,confidentiel,country,city,lat,lng
    CSV.foreach(file, :headers => true) do |row|
      Internship.create({
        id: row[0],
        address: row[1],
        branch_abbreviation: row[2],
        filiere: row[3],
        company: row[4],
        description: row[5],
        student: row[6],
        level_abbreviation: row[7],
        semester: row[8],
        year: row[9],
        subject: row[10],
        teacher: row[11],
        done: row[12] == "x" ? true : false,
        confidential: row[13] == "x" ? true : false,
        country: row[14],
        city: row[15],
        latitude: row[16],
        longitude: row[17]
      })
    end
  end
end