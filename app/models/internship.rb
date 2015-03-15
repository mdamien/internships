class Internship < ActiveRecord::Base
  scope :from_year, -> (year) { where("year >= ?", year) }
  scope :to_year, -> (year) { where("year <= ?", year) }

  def self.order_internships(internships)
    return internships
               .order(year: :DESC)
               .order(semester: :DESC)
               .order(country: :ASC)
               .order(company: :ASC)
  end

  def self.most_recent_internships
    most_recent_year = Internship.maximum("year")
    return order_internships(Internship.from_year(most_recent_year))
  end

  def self.search query
    if query.has_key?(:from_year) && query.has_key?(:to_year) && query.has_key?(:from_semester) && query.has_key?(:to_semester)
      internships = from_year(query[:from_year]).to_year(query[:to_year])

      if query[:from_semester] == 'A'
        #Removing spring internship of from_year.
        internships = internships.where.not("semester LIKE '%P%' and year = ?", query[:from_year])
      end
      if query[:to_semester] == 'P'
        #Removing fall internship of from_year.
        internships = internships.where.not("semester LIKE '%A%' and year = ?", query[:to_year])
      end

      return order_internships(internships)
    end

    # Returning most recent internships if missing parameters.
    return most_recent_internships
  end

  def self.allInternshipYears
    return select(:year).distinct.order(year: :ASC)
  end
end