class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  
  def index
    @internships = Internship.all
  end
  
  def view
    @internship = Internship.find(params[:id])
  end
end
