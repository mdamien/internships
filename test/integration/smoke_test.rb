require 'test_helper'

class TestController < ApplicationController
  def index; end
end

class AppControllerTest < ActionController::TestCase

  setup do
    @controller = ApplicationController.new
  end
  
  test "homepage is working" do
    get :index
    assert_response :success
    assert_select 'title', "Stages UTC"
  end

end